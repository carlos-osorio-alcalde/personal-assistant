from dataclasses import dataclass
from typing import List


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
class SyllabeAssesmentResult:
    """
    This class represents the word assesment result of a given audio file.
    """

    syllabe: str
    accuracy_score: float


@dataclass
class WordAssesmentResult:
    """
    This class represents the word assesment result of a given audio file.
    """

    word: str
    syllabes: List[SyllabeAssesmentResult]
    accuracy_score: float
