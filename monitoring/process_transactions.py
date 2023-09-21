import datetime
import os
from typing import List, Literal, Union

import pandas as pd
import pytz
import requests
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from numpy import average

from monitoring.email import send_email

# Load environment variables
load_dotenv()


def get_transactions(
    return_as_pandas: bool = False,
) -> Union[List[dict], pd.DataFrame]:
    """
    This function returns the transactions of the current day.

    Parameters
    ----------
    return_as_pandas : bool, optional
        Whether to return the transactions as a pandas DataFrame or not,
        by default False

    Returns
    -------
    pd.DataFrame
        The dataframe with all the transactions of the current day.
    """
    # Get the transactions of the current day
    url = f"https://personal-expenses.purplesky-efe9a7f4.eastus.azurecontainerapps.io/expenses/get_full_transactions_day/"  # noqa
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('API_EXPENSES_TOKEN')}",
    }
    response = requests.get(url, headers=headers)

    # Return the transactions as a DataFrame
    df_transactions = pd.DataFrame(response.json())
    return (
        df_transactions[
            df_transactions["transaction_type"].isin(
                ["Compra", "Transferencia", "QR"]
            )
        ]
        if return_as_pandas
        else [
            transaction
            for transaction in response.json()
            if transaction["transaction_type"]
            in ["Compra", "Transferencia", "QR"]
        ]
    )


def compute_daily_values(transactions: pd.DataFrame) -> dict:
    """
    Compute the daily values of expenses to pass through the anomaly model.

    Parameters
    ----------
    transactions : pd.DataFrame
        The transactions of the current day.

    Returns
    -------
    dict
        The dictionary with the needed values
    """
    expenses_values = {
        "avg_amount": (-1) * transactions["amount"].mean(),
        "max_amount": (-1) * transactions["amount"].max(),
        "total_trx": transactions.shape[0],
        "weekend": "yes"
        if datetime.datetime.now()
        .astimezone(pytz.timezone("America/Bogota"))
        .isoweekday()
        in [6, 7]
        else "no",
    }
    return expenses_values


def check_anomaly(expenses_values: dict) -> Literal["normal", "anomaly"]:
    """
    Make the request to check if the daily values are an anomaly.

    Parameters
    ----------
    expenses_values : dict
        The dictionary with the needed values

    Returns
    -------
    Literal["normal", "anomaly"]
        Whether the values are an anomaly or not.
    """
    params = {
        "avg_amount": expenses_values["avg_amount"],
        "max_amount": expenses_values["max_amount"],
        "total_trx": expenses_values["total_trx"],
        "weekend": expenses_values["weekend"],
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('API_EXPENSES_TOKEN')}",
    }
    response = requests.get(
        "https://personal-expenses.purplesky-efe9a7f4.eastus.azurecontainerapps.io/monitoring/predict_anomaly",  # noqa
        params=params,
        headers=headers,
    )
    return response.json()["prediction"]


def create_html_email(transactions: List[dict]) -> str:
    """
    Create the html email to send.

    Parameters
    ----------
    transactions : List[dict]
        The transactions of the current day.

    Returns
    -------
    str
        The html email to send.
    """
    # Check the day status
    day_status = check_anomaly(
        compute_daily_values(pd.DataFrame(transactions))
    )

    # Create a Jinja2 environment with a template loader
    env = Environment(loader=FileSystemLoader("monitoring/static/"))

    # Load your HTML template
    template = env.get_template("base.html")

    # Define the data and format amount as $0.00
    transactions_short = [
        {
            "transaction_type": transaction["transaction_type"],
            "merchant": transaction["merchant"],
            "amount": f"${transaction['amount']:.2f}",
        }
        for transaction in transactions
    ]

    summary = {
        "num_transactions": len(transactions_short),
        "sum_transactions": sum(
            [transaction["amount"] for transaction in transactions_short]
        ),
        "avg_amount": average(
            [transaction["amount"] for transaction in transactions_short]
        ),
    }

    # Render the template with the data
    rendered_template = template.render(
        transactions=transactions_short,
        summary=summary,
        day_status=day_status,
    )

    return rendered_template


if __name__ == "__main__":
    # Get the transactions
    gross_transactions = get_transactions(return_as_pandas=False)
    html = create_html_email(gross_transactions)

    # Send the email
    send_email(html)
