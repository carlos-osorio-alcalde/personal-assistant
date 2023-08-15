import os

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

# Get the speech key and service region from the environment variables
speech_key, service_region = os.getenv(
    "AZURE_SPEECH_SUBSCRIPTION_KEY"
), os.getenv("SPEECH_REGION")


class VoiceSintetizer:
    def __init__(
        self, voice: str = "en-US-AshleyNeural", file_to_save: str = None
    ):
        self._voice = voice
        self._output_file = file_to_save
        self._speech_synthesizer = self._get_sintetizer()

    def _get_sintetizer(self) -> speechsdk.SpeechSynthesisResult:
        """
        This function sintetizes a given text and returns the sintetized
        audio.

        Parameters
        ----------
        text : str
            The text to sintetize.

        Returns
        -------
        speechsdk.SpeechSynthesisResult
            The speech sintetized object.
        """
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=service_region
        )

        file_config = speechsdk.audio.AudioOutputConfig(
            filename=self._output_file
        )

        # Set the voice name
        speech_config.speech_synthesis_voice_name = self._voice

        # Creates a speech synthesizer
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=file_config
        )

        return self.speech_synthesizer

    def sintetize_text(self, text: str) -> speechsdk.AudioDataStream | None:
        """
        This function sintetizes a given text and returns the sintetized
        audio.

        Parameters
        ----------
        text : str
            The text to sintetize.

        Returns
        -------
        speechsdk.AudioDataStream
            The audio data stream with the sintetized audio.
        """
        # Synthesizes the received text to speech.
        result = self.speech_synthesizer.speak_text_async(text).get()
        return result if text is not None else None
