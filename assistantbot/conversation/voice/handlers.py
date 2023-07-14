from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from pathlib import Path
import soundfile as sf
from typing import Optional, Literal

from langchain.chains import ConversationChain
from assistantbot.conversation.base import ConversationHandler
from assistantbot.conversation.text.handlers import TextHandler
from assistantbot.ai.voice.whisper import transcript_audio
from assistantbot.ai.voice.pronunciation import PronunciationAssessment
from assistantbot.ai.text.prompts.pronunciation import (
    GLOBAL_PRONUNCIATION_ASSESSMENT,
    WORDS_PRONUNCIATION_ASSESSMENT_BASE,
    WORD_PRONUNCIATION_ASSESSMENT_PARTICULAR,
)


class VoiceHandler(ConversationHandler):
    def __init__(
        self,
        conversation_chain: Optional[ConversationChain] = None,
        grading_system: Optional[
            Literal["hundred_mark", "five_points"]
        ] = "hundred_mark",
        granularity: Optional[Literal["phoneme", "word", "full"]] = "word",
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
            chat_id=update.effective_chat.id, action="typing"
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

        # Get the final response concatenating the response_message with the
        # pronunciation assessment

        # Get the pronunciation assessment
        assessment_message = self._get_pronuntiation_assessment_response(
            entry_message, f"{output_file}.wav"
        )

        # Send the response message
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message + "\n\n" + assessment_message,
            parse_mode="HTML",
        )

        # Delete the .wav files
        Path(f"{output_file}.wav").unlink()

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
        assessment_result = self.pronuntiation_assessment.get_assessment(
            reference_text, input_audio_path
        )

        # Get the global assessment result
        global_assessment = self.pronuntiation_assessment.get_global_scores(
            assessment_result
        )

        # Get the word assessment result
        word_assessment = self.pronuntiation_assessment.get_words_scores(
            assessment_result
        )

        # Create the assessment string for global assessment
        assessment_global_string = GLOBAL_PRONUNCIATION_ASSESSMENT.format(
            phrase=reference_text,
            pronunciation_score=global_assessment.pronunciation_score,
            accuracy_score=global_assessment.accuracy_score,
            fluency_score=global_assessment.fluency_score,
        )

        # Create the assessment string for word assessment
        assessment_words_string = WORDS_PRONUNCIATION_ASSESSMENT_BASE

        for word in word_assessment:
            if word.accuracy_score < 0.9:
                assessment_words_string += (
                    WORD_PRONUNCIATION_ASSESSMENT_PARTICULAR.format(
                        word=word.word,
                        accuracy_score=word.accuracy_score,
                    )
                )
        # If the pronunciation of all the words was ok, don't send that part
        # of the assessment.
        if assessment_words_string == WORDS_PRONUNCIATION_ASSESSMENT_BASE:
            assessment_words_string = ""

        return assessment_global_string + assessment_words_string
