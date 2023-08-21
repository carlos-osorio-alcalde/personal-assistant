from pathlib import Path
from typing import Literal, Optional

import soundfile as sf
from langchain.chains import ConversationChain
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.ai.text.prompts.pronunciation import (
    GLOBAL_PRONUNCIATION_ASSESSMENT,
    WORD_PRONUNCIATION_ASSESSMENT_PARTICULAR,
    WORDS_PRONUNCIATION_ASSESSMENT_BASE,
)
from assistantbot.ai.voice.pronunciation import PronunciationAssessment
from assistantbot.ai.voice.sintetizer import VoiceSintetizer
from assistantbot.ai.voice.whisper import transcript_audio
from assistantbot.conversation import TextHandler
from assistantbot.conversation.base import ConversationHandler


class VoiceHandler(ConversationHandler):
    def __init__(
        self,
        conversation_chain: Optional[ConversationChain] = None,
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
        conversation_chain : Optional[ConversationChain], optional
            In order to maintain the conversation, the bot needs to know
            the conversation chain. If this parameter is not specified,
            the bot will use the default conversation chain, by default None
        """
        super().__init__(filters.VOICE)
        self.conversation_chain = conversation_chain
        self.pronuntiation_assessment = PronunciationAssessment(
            grading_system=grading_system, granularity=granularity
        )

    def handler(self) -> MessageHandler:
        return MessageHandler(self._type, self.callback)

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
        entry_message = self._transcript_voice_message(f"{output_file}.wav")
        response_message = self._create_text_response(entry_message)

        # Get the final response with the voice message and the
        # pronunciation assessment

        # Get the pronunciation assessment
        assessment_message = self._get_pronuntiation_assessment_response(
            entry_message, f"{output_file}.wav"
        )

        # Send the response message via voice
        voice_sintetizer = VoiceSintetizer(
            file_to_save=f"{output_file}_response.wav"
        )
        voice_sintetizer.sintetize_text(response_message)

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
    def _transcript_voice_message(input_file: str) -> str:
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
        transcription = transcript_audio(input_file)
        return transcription

    def _create_text_response(self, entry_message: str) -> str:
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
        # If the conversation chain is not specified, use the default one
        # However, this should not happen
        if self.conversation_chain is None:
            self.conversation_chain = TextHandler().conversation_chain

        response_message = self.conversation_chain.predict(
            input=entry_message
        )
        return response_message

    def _get_pronuntiation_assessment_response(
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
        ) = self.pronuntiation_assessment.get_assessment(
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
