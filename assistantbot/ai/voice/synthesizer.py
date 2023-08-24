import os
from typing import Union

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class VoiceSynthesizer:
    def __init__(
        self,
        voice: str = "en-US-SaraNeural",
        style: str = "cheerful",
        file_to_save: str = None,
    ):
        """
        This class sintetizes a given text and returns the synthetized
        audio.
        """
        self._voice = voice
        self._style = style
        self._output_file = file_to_save
        self._speech_synthesizer = self._get_synthetizer()

    def _get_synthetizer(self) -> speechsdk.SpeechSynthesisResult:
        """
        This function synthetizes a given text and returns the synthetized
        audio.

        Parameters
        ----------
        text : str
            The text to synthetized.

        Returns
        -------
        speechsdk.SpeechSynthesisResult
            The speech synthetized object.
        """
        speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_SUBSCRIPTION_KEY"),
            region=os.getenv("SPEECH_REGION"),
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

    def _create_ssl(self, text: str) -> str:
        """
        This method creates a speech synthesis markup language (SSML) string
        with the given text and style.

        Parameters
        ----------
        text : str
            The text to sintetize.

        Returns
        -------
        str
            The SSML string.
        """
        head1 = f'<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="{self._voice}"><s />'  # noqa
        head2 = f'<mstts:express-as style="{self._style}"> {text} </mstts:express-as><s /></voice></speak>'  # noqa

        return head1 + head2

    async def synthetize_text(
        self, text: str
    ) -> Union[speechsdk.AudioDataStream, None]:
        """
        This function sintetizes a given text and returns the synthetized
        audio.

        Parameters
        ----------
        text : str
            The text to synthetize.

        Returns
        -------
        speechsdk.AudioDataStream
            The audio data stream with the synthetize audio.
        """
        # Synthesizes the received text to speech.
        result = self.speech_synthesizer.speak_ssml_async(
            self._create_ssl(text)
        ).get()

        return result if text is not None else None
