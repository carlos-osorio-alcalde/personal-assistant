import requests
import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()


def get_random_word() -> Dict:
    """
    This function gets a random word from the Words API.

    Returns
    -------
    Dict
        The random word with some information.
    """
    url = "https://wordsapiv1.p.rapidapi.com/words/"

    querystring = {"random": "true"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring).json()

    return {
        "word": response["word"],
        "definition": response["results"][0]["definition"]
        if response.get("results")
        else "",
    }
