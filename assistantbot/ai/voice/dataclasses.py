from dataclasses import dataclass


@dataclass
class GlobalAssesmentResult:
    """
    This class represents the global assesment result of a given audio file.
    """

    accuracy_score: float
    pronunciation_score: float
    completeness_score: float
    fluency_score: float


@dataclass
class WordAssesmentResult:
    """
    This class represents the word assesment result of a given audio file.
    """

    word: str
    accuracy_score: float
