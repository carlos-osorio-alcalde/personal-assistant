import os
from typing import List, Literal, Optional

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

from .dataclasses import GlobalAssesmentResult, WordAssesmentResult

load_dotenv()

# Get the speech key and service region from the environment variables
speech_key, service_region = os.getenv(
    "AZURE_SPEECH_SUBSCRIPTION_KEY"
), os.getenv("SPEECH_REGION")


class PronunciationAssessment:
    def __init__(
        self,
        grading_system: Optional[
            Literal["hundred_mark", "five_points"]
        ] = "hundred_mark",
        granularity: Optional[Literal["phoneme", "word", "full"]] = "word",
    ):
        """
        This class performs the pronunciation assessment of a given audio
        file

        Parameters
        ----------
        grading_system : Optional[ Literal['hundred_mark', 'five_points']]
            The grading system to use, by default "hundred_mark"
        granularity : Optional[Literal['phoneme';, 'word';, 'full']]
            The granularity of the assesment, by default "word"
        """
        self.assessment = None

        # Set the grading system and the granularity
        base_grading = speechsdk.PronunciationAssessmentGradingSystem
        base_granularity = speechsdk.PronunciationAssessmentGranularity

        if grading_system == "hundred_mark":
            self.grading_system = base_grading.HundredMark
        elif grading_system == "five_points":
            self.grading_system = base_grading.FivePoint

        if granularity == "phoneme":
            self.granularity = base_granularity.Phoneme
        elif granularity == "word":
            self.granularity = base_granularity.Word
        elif granularity == "full":
            self.granularity = base_granularity.FullText

    def get_assessment(
        self, reference_text: str, input_audio_path: str
    ) -> speechsdk.PronunciationAssessmentResult:
        """
        This function performs the pronunciation assessment of a given audio
        file and returns the assessment.

        Parameters
        ----------
        reference_text : str
            The reference text to compare the audio file with.

        input_audio_path : str
            The path to the audio file.
        """
        # Create the speech config
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=service_region
        )
        audio_config = speechsdk.audio.AudioConfig(filename=input_audio_path)

        # create pronunciation assessment config, set grading system,
        # granularity and if enable miscue based on your requirement.
        pronunciation_assessment_config = (
            speechsdk.PronunciationAssessmentConfig(
                reference_text=reference_text,
                grading_system=self.grading_system,
                granularity=self.granularity,
            )
        )

        # Creates a speech recognizer using a file as audio input.
        language = "en-US"
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            language=language,
            audio_config=audio_config,
        )
        # apply pronunciation assessment config to speech recognizer
        pronunciation_assessment_config.apply_to(speech_recognizer)

        assessment_result = speech_recognizer.recognize_once()
        if (
            assessment_result.reason
            == speechsdk.ResultReason.RecognizedSpeech
        ):
            return speechsdk.PronunciationAssessmentResult(assessment_result)
        else:
            raise Exception("The assessment was not performed correctly.")

    @staticmethod
    def get_global_scores(
        pronunciation_result: speechsdk.PronunciationAssessmentResult,
    ) -> GlobalAssesmentResult:
        """
        This function returns the global scores of the assessment.

        Parameters
        ----------
        reference_text : str
            The reference text to compare the audio file with.

        input_audio_path : str
            The path to the audio file.
        """
        return GlobalAssesmentResult(
            accuracy_score=pronunciation_result.accuracy_score,
            pronunciation_score=pronunciation_result.pronunciation_score,
            completeness_score=pronunciation_result.completeness_score,
            fluency_score=pronunciation_result.fluency_score,
        )

    @staticmethod
    def get_words_scores(
        pronunciation_result: speechsdk.PronunciationAssessmentResult,
    ) -> List[WordAssesmentResult]:
        """
        This function returns the word assessment of the assessment.

        Parameters
        ----------
        assessment_result : speechsdk.SpeechRecognitionResult
            The assessment result.

        Returns
        -------
        List[WordAssesmentResult]
            The list of word assessment results.
        """
        words_results = [
            WordAssesmentResult(
                word=word.word, accuracy_score=word.accuracy_score
            )
            for word in pronunciation_result.words
        ]
        return words_results
