from pathlib import Path
from typing import Literal, Optional

import soundfile as sf
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.ai.text.prompts.pronunciation import (
    GLOBAL_PRONUNCIATION_ASSESSMENT,
    WORD_PRONUNCIATION_ASSESSMENT_PARTICULAR,
    WORDS_PRONUNCIATION_ASSESSMENT_BASE,
)
from assistantbot.ai.voice.pronunciation import PronunciationAssessment
from assistantbot.ai.voice.synthesizer import VoiceSynthesizer
from assistantbot.ai.voice.whisper import transcript_audio
from assistantbot.conversation.base import ConversationHandler
from assistantbot.conversation.chains import (
    get_conversation_chain,
    update_memory,
)


class VoiceHandler(ConversationHandler):
    def __init__(
        self,
        grading_system: Optional[
            Literal["hundred_mark", "five_points"]
        ] = "hundred_mark",
        granularity: Optional[
            Literal["phoneme", "word", "full"]
        ] = "phoneme",
    ):
        """
        This class handles the voice messages sent to the bot.

        Parameters
        ----------
        grading_system : Optional[Literal["hundred_mark", "five_points"]]
            The grading system to use for the pronunciation assessment,

        granularity : Optional[Literal["phoneme", "word", "full"]], optional
            The granularity to use for the pronunciation assessment,
        """
        super().__init__(filters.VOICE)
        self.pronuntiation_assessment = PronunciationAssessment(
            grading_system=grading_system, granularity=granularity
        )

    def handler(self) -> MessageHandler:
        """
        This function returns the message handler.

        Returns
        -------
        MessageHandler
            The message handler.
        """
        return MessageHandler(self._type, self.callback, block=False)

    async def callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        This function is called when a voice message is sent to the bot.

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : _type_
            The context object from Telegram.
        """
        # If a voice message is sent, the bot will reply with a text message
        # containing the text of the voice message.
        voice_file = update.message.voice

        # Send the typing action
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="record_voice",
            read_timeout=20,
            write_timeout=20,
        )

        # Get the voice message
        voice_file = await context.bot.get_file(voice_file.file_id)

        # Save the file in the folder temp of the same directory of this file
        output_file = (
            f"{Path(__file__).parent.absolute()}/temp/"
            f"{voice_file.file_unique_id}"
        )

        # Download the file
        await voice_file.download_to_drive(f"{output_file}.ogg")

        # Convert the downloaded .ogg file to .wav
        self._process_incoming_audio(
            f"{output_file}.ogg", f"{output_file}.wav"
        )

        # Obtain response message
        entry_message = await self._transcript_voice_message(
            f"{output_file}.wav"
        )
        response_message = await self._create_text_response(
            update.effective_user.id, entry_message
        )

        # Get the final response with the voice message and the
        # pronunciation assessment
        # Get the pronunciation assessment
        assessment_message = (
            await self._get_pronuntiation_assessment_response(
                entry_message, f"{output_file}.wav"
            )
        )

        # Send the response message via voice
        voice_sintetizer = VoiceSynthesizer(
            file_to_save=f"{output_file}_response.wav"
        )
        await voice_sintetizer.sintetize_text(response_message)

        # Send the voice message
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=open(f"{output_file}_response.wav", "rb"),
            title="This is my response",
            caption=response_message[0:1024],
        )

        # Send the assessment message
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=assessment_message,
            parse_mode="HTML",
        )

        # Delete the .wav files
        Path(f"{output_file}.wav").unlink()
        Path(f"{output_file}_response.wav").unlink()

    @staticmethod
    def _process_incoming_audio(input_file: str, output_file: str) -> None:
        """
        This function converts an audio file to .wav format and saves it in
        the specified output file.

        Parameters
        ----------
        input_file : str
            The input audio file.
        output_file : str
            The output audio file.
        """
        # Convert the audio file to .wav
        data, samplerate = sf.read(input_file)
        sf.write(output_file, data, samplerate)

        # Delete the input file
        Path(input_file).unlink()

    @staticmethod
    async def _transcript_voice_message(input_file: str) -> str:
        """
        This function transcripts the voice message and returns the text
        using Whisper API.

        Parameters
        ----------
        input_file : str
            The input audio file.

        Returns
        -------
        str
            The text of the voice message.
        """
        transcription = await transcript_audio(input_file)
        return transcription

    async def _create_text_response(
        self, user_id: int, entry_message: str
    ) -> str:
        """
        This function creates the text response using the handler of the
        text conversation.

        Parameters
        ----------
        entry_message : str
            The text of the voice message.

        Returns
        -------
        str
            The text response.
        """
        # Get the conversation chain
        conversation_chain = get_conversation_chain(user_id)

        response_message = await conversation_chain.apredict(
            input=entry_message
        )

        # Update the memory
        update_memory(user_id, conversation_chain)

        return response_message

    async def _get_pronuntiation_assessment_response(
        self, reference_text: str, input_audio_path: str
    ) -> str:
        """
        This function performs the pronunciation assessment of a given audio
        file and returns the assessment.

        Parameters
        ----------
        reference_text : str
            The reference text to use for the assessment.
        input_audio_path : str
            The path of the input audio file.

        Returns
        -------
        str
            The string with the assessment of the pronunciation.
        """
        (
            json_recognition_result,
            assessment_result,
        ) = await self.pronuntiation_assessment.get_assessment(
            reference_text, input_audio_path
        )

        # Get the global assessment result
        global_assessment = self.pronuntiation_assessment.get_global_scores(
            assessment_result
        )

        # Get the word assessment result
        word_assessment = self.pronuntiation_assessment.get_words_scores(
            json_recognition_result
        )

        # Create the assessment string for word assessment
        assessment_words_string = WORDS_PRONUNCIATION_ASSESSMENT_BASE
        tagged_text = ""

        for word in word_assessment:
            # If there is a word with a bad pronunciation, add it to the
            # assessment string
            if word.accuracy_score <= 95:
                # Get the string of the syllabes
                syllabes_string = "".join(
                    f"{s.syllabe} ({s.accuracy_score}) "
                    for s in word.syllabes
                )

                assessment_words_string += (
                    WORD_PRONUNCIATION_ASSESSMENT_PARTICULAR.format(
                        word=word.word, syllabes_string=syllabes_string
                    )
                )

            # Add the word to the colored text
            if word.accuracy_score >= 95:
                tag = "i"
            elif word.accuracy_score >= 90:
                tag = "u"
            else:
                tag = "s"
            tagged_text += f"<{tag}>{word.word}</{tag}> "

        # Create the assessment string for global assessment
        assessment_global_string = GLOBAL_PRONUNCIATION_ASSESSMENT.format(
            phrase=tagged_text,
            pronunciation_score=global_assessment.pronunciation_score,
            accuracy_score=global_assessment.accuracy_score,
            fluency_score=global_assessment.fluency_score,
        )

        if assessment_words_string == WORDS_PRONUNCIATION_ASSESSMENT_BASE:
            # If there are no words with a bad pronunciation, return only the
            # global assessment
            assessment_words_string = (
                "\n Nice! You pronounced all" " the words correctly!"
            )

        return assessment_global_string + assessment_words_string
