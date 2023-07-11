import os
from typing import Dict

import requests
from dotenv import load_dotenv

from assistantbot.configuration import config

# Load environment variables
load_dotenv()


class RandomWord:
    def __init__(self):
        self._word = self._get_random_word()
        self._definition = self._get_definition()

    def _get_random_word(self) -> str:
        """
        This function gets a random word from the WordNik API.

        Returns
        -------
        Dict
            The random word with some information.
        """
        url = "https://api.wordnik.com/v4/words.json/randomWord"

        querystring = {
            "hasDictionaryDef": "true",
            "minDictionaryCount": "1",
            "maxDictionaryCount": "-1",
            "minLength": "5",
            "maxLength": "12",
            "api_key": os.getenv("WORDNIK_API_KEY"),
        }

        headers = {
            "Accept": "application/json",
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=config["TIMEOUT"],
        )

        return response.json()["word"] if response.status_code == 200 else ""

    def _get_definition(self) -> str:
        """
        This function gets the definition of a word from the Words API.

        Returns
        -------
        str
            The definition of the word.
        """
        url = (
            "https://api.wordnik.com/v4/word.json/"
            f"{self._word}/definitions"
        )

        querystring = {
            "limit": 3,
            "includeRelated": "false",
            "sourceDictionaries": "all",
            "useCanonical": "false",
            "includeTags": "false",
            "api_key": os.getenv("WORDNIK_API_KEY"),
        }

        headers = {
            "Accept": "application/json",
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=config["TIMEOUT"],
        )

        return (
            response.json()[0]["text"] if response.status_code == 200 else ""
        )

    def get_random_word(self) -> Dict[str, str]:
        """
        This function returns the random word and its definition.

        Returns
        -------
        Dict[str, str]
            The random word and its definition.
        """
        return {"word": self._word, "definition": self._definition}
