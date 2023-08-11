import datetime
import os
from typing import List, Union

import pyodbc
from dotenv import load_dotenv

from expenses.processors.schemas import TransactionInfo

# Check if the file exists
if os.path.exists("expenses/.env"):
    load_dotenv(dotenv_path="expenses/.env")


def get_cursor() -> Union[pyodbc.Cursor, None]:
    """
    This function creates a connection to the database.

    Returns
    -------
    pyodbc.Connection
        The connection to the database.
    """
    try:
        # Establish the connection
        conn = pyodbc.connect(
            f"""DRIVER=ODBC Driver 18 for SQL Server;\
            SERVER={os.getenv("SERVER")};\
            DATABASE={os.getenv("DATABASE")};\
            UID={os.getenv("USERNAME")};\
            PWD={os.getenv("PASSWORD")}"""
        )
        cursor = conn.cursor()
        return cursor
    except Exception:
        return None


def get_transactions_from_database(
    date_from: datetime.datetime,
) -> List[TransactionInfo]:
    """
    Searches for the transactions in the database given a date.

    Parameters
    ----------
    date_from : datetime.datetime
        The date to search.

    Returns
    -------
    List[TransactionInfo]
        The list of transactions.
    """
    try:
        cursor = get_cursor()

        # Get the transactions
        cursor.execute(
            """
            SELECT
                transaction_type,
                amount,
                merchant,
                datetime,
                payment_method,
                email_log_id
            FROM transactions
            WHERE datetime >= ?
            """,
            date_from.date(),
        )
        transactions_from_db = cursor.fetchall()

        # Close the connection
        cursor.close()

        # Get the transactions with the correct type
        if len(transactions_from_db) > 0:
            transactions = [
                TransactionInfo(
                    transaction_type=str(transaction[0]),
                    amount=transaction[1],
                    merchant=str(transaction[2]),
                    datetime=transaction[3],
                    paynment_method=str(transaction[4]),
                    email_log=transaction[5],
                )
                for transaction in transactions_from_db
            ]
        else:
            transactions = []

        return transactions
    except Exception:
        return []
