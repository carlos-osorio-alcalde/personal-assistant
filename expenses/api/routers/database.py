import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from expenses.api.schemas import AddTransactionInfo
from expenses.api.security import check_access_token
from expenses.api.utils import (
    get_cursor,
    get_date_from_search,
    get_query_to_insert_values,
    get_transactions,
)

router = APIRouter(prefix="/database")

# Check if the file exists
if os.path.exists("expenses/.env"):
    load_dotenv(dotenv_path="expenses/.env")


@router.get("/test_connection", dependencies=[Depends(check_access_token)])
def test_connection() -> str:
    """
    This function tests the connection to the database.

    Returns
    -------
    str
        A message indicating the status of the connection.
    """
    try:
        # Establish the connection
        cursor = get_cursor()
        # Obtain the rows
        cursor.execute("SELECT TOP 1 * FROM transactions")
        rows = cursor.fetchall()
        cursor.close()
        return f"Connection successful. This is the first row: {str(rows)}"
    except Exception:
        raise HTTPException(status_code=500, detail="Connection failed.")


@router.post(
    "/populate_table/", dependencies=[Depends(check_access_token)]
)
def populate_table(
    timeframe: Literal["daily", "weekly", "partial_weekly", "monthly"]
) -> str:
    """
    This function populates the transactions table.

    Parameters
    ----------
    timeframe : Literal["daily", "weekly", "partial_weekly", "monthly"]
        The timeframe to obtain the expenses from.

    Returns
    -------
    str
        A message indicating the status of the connection.
    """
    # Check if the timeframe is valid
    if timeframe not in ["daily", "weekly", "partial_weekly", "monthly"]:
        raise HTTPException(
            status_code=400,
            detail="The timeframe must be daily, weekly, partial_weekly or "
            "monthly",
        )

    try:
        # Get the date to search
        date_to_search = get_date_from_search(timeframe)

        # Process the transactions
        transactions = get_transactions(date_to_search)

        # Establish the connection
        cursor = get_cursor()

        # Prepare the data for insertion
        insert_values = [
            (
                transaction.transaction_type,
                transaction.amount,
                transaction.merchant,
                transaction.datetime.date(),
                transaction.paynment_method,
                transaction.email_log,
            )
            for transaction in transactions
        ]

        try:
            for values in insert_values:
                cursor.execute(
                    get_query_to_insert_values(), values + values[:-1]
                )
                cursor.commit()

            cursor.close()
        except Exception:
            raise HTTPException(status_code=500, detail="Insertion failed.")

        return "Table populated successfully."
    except Exception:
        raise HTTPException(status_code=500, detail="Connection failed.")


@router.post("/add_transaction", dependencies=[Depends(check_access_token)])
async def add_transaction(transaction: AddTransactionInfo) -> str:
    """
    This function adds a transaction to the database.

    Parameters
    ----------
    transaction : AddTransactionInfo
        The transaction to add.

    Returns
    -------
    str
        A message indicating the status of the connection.
    """
    try:
        # Establish the connection
        cursor = get_cursor()

        if transaction.transaction_type != "Compra":
            raise HTTPException(
                status_code=501,
                detail="Right now, only purchases are supported.",
            )

        # Prepare the data for insertion
        values = (
            transaction.transaction_type,
            transaction.amount,
            transaction.merchant,
            transaction.datetime.date(),
            transaction.paynment_method,
            transaction.email_log,
        )

        try:
            cursor.execute(
                get_query_to_insert_values(), values + values[:-1]
            )
            cursor.commit()

            cursor.close()
        except Exception:
            raise HTTPException(status_code=500, detail="Insertion failed.")

        return "Transaction added successfully."
    except Exception:
        raise HTTPException(status_code=500, detail="Connection failed.")
