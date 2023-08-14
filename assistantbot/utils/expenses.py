import requests
from dotenv import load_dotenv
import os
from typing import Literal, Tuple

# Load environment variables
load_dotenv()


def get_expenses(
    timeframe: Literal["daily", "weekly", "partial_weekly", "monthly"]
) -> str:
    """
    This function returns the summary of the expenses of the day or the week

    Parameters
    ----------
    timeframe : Literal["daily", "weekly", "partial_weekly", "monthly"]
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
    expenses = response.json()
    expenses_str = ""
    for _, values_expenses in expenses.items():
        if values_expenses["name"]:
            expenses_str += (
                f"{values_expenses['name']}, "
                f"amount: ${abs(values_expenses['amount'])}, "
                f"count: {values_expenses['count']} \n"
            )

    return expenses_str if expenses_str else "No expenses found."


def get_expenses_a_day_like_today() -> Tuple[float, float]:
    """
    This function returns the mean number of purchases and the median amount
    of purchases of a day like today.

    Returns
    -------
    Tuple[float, float]
        The mean number of purchases and the median amount of purchases of a
        day like today.
    """
    url = "https://personal-expenses.purplesky-efe9a7f4.eastus.azurecontainerapps.io/expenses/a_day_like_today/"  # noqa
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + os.getenv("API_EXPENSES_TOKEN"),
    }
    response = requests.get(url, headers=headers)

    # Check if the response is correct
    if response.status_code != 200:
        return 0, 0

    # Get the json response
    json_response = response.json()
    return (
        json_response["mean_number_of_purchases"],
        abs(json_response["median_amount_of_purchases"]),
    )


if __name__ == "__main__":
    print(get_expenses_a_day_like_today())
