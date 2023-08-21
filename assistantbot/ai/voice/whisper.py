import os
from pathlib import Path

import openai


def transcript_audio(audio_file: str) -> str:
    """
    This function uses the OpenAI API to transcript the audio file and
    returns the text.

    Parameters
    ----------
    audio_file : str
        The audio file path.

    Returns
    -------
    str
        The text of the audio file.
    """
    # Check if the audio file exists
    if not Path(audio_file).exists():
        raise FileNotFoundError(f"The file {audio_file} does not exist")

    # Set the OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    transcript = openai.Audio.transcribe(
        "whisper-1", file=open(audio_file, "rb"), language="en"
    )

    return transcript["text"]
