import requests
from dotenv import load_dotenv
import os
import json
from typing import Literal

# Load environment variables
load_dotenv()


def get_expenses(timeframe: Literal["daily", "weekly"]) -> str:
    """
    This function returns the summary of the expenses of the day or the week

    Parameters
    ----------
    timeframe : Literal["daily", "weekly"]
        The timeframe to obtain the expenses from.

    Returns
    -------
    str
        The summary of the expenses of the day or the week.
    """
    url = f"https://personal-expenses.purplesky-efe9a7f4.eastus.azurecontainerapps.io/expenses/{timeframe}"  # noqa
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + os.getenv("API_EXPENSES_TOKEN"),
    }
    response = requests.get(url, headers=headers)

    # Check if the response is correct
    if response.status_code != 200:
        return "Ups, something went wrong."

    # Convert the json to a string
    return json.dumps(response.json(), indent=2, sort_keys=True)


if __name__ == "__main__":
    print(get_expenses("daily"))
