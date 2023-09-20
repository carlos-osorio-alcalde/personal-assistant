import datetime
from typing import List, Literal

import pytz
from fastapi import APIRouter, Depends

from expenses.api.schemas import SummaryADayLikeToday, SummaryTransactionInfo
from expenses.api.security import check_access_token
from expenses.api.utils import (
    get_date_from_search,
    get_summary_a_day_like_today,
    get_transactions,
    get_transactions_from_database,
    process_transactions_api_expenses,
)
from expenses.processors.schemas import TransactionInfo

router = APIRouter(prefix="/expenses")


# Function to get the transactions from the database
def get_gross_transactions(
    timeframe: Literal["daily", "weekly", "partial_weekly", "monthly"]
) -> List[TransactionInfo]:
    """
    This function returns the full transactions of the current timeframe

    Returns
    -------
    List[TransactionInfo]
        The summary of the expenses of the day, week or month.
    """
    # Get the date to search
    date_to_search = get_date_from_search(timeframe)

    # Search in the database for the transactions
    transactions_from_db = get_transactions_from_database(date_to_search)

    # If there are not transactions in the database, search in the API
    # and process the transactions.
    transactions = (
        transactions_from_db
        if len(transactions_from_db) > 0
        else get_transactions(date_to_search)
    )

    return transactions


# Create the endpoint to get the summary of the expenses of the day, week or
# month
@router.get(
    "/{timeframe}",
    response_model=SummaryTransactionInfo,
    dependencies=[Depends(check_access_token)],
)
async def get_expenses(
    timeframe: Literal["daily", "weekly", "partial_weekly", "monthly"]
) -> SummaryTransactionInfo:
    """
    This function returns the summary of the expenses of the day, week or
    month.

    Parameters
    ----------
    timeframe : Literal["daily", "weekly", "partial_weekly", "monthly"]
        The timeframe to obtain the expenses from.

    Returns
    -------
    SummaryTransactionInfo
        The summary of the expenses of the day, week or month.
    """
    return process_transactions_api_expenses(
        get_gross_transactions(timeframe)
    )


@router.get(
    "/a_day_like_today/",
    response_model=SummaryADayLikeToday,
    dependencies=[Depends(check_access_token)],
)
async def get_expenses_a_day_like_today() -> SummaryADayLikeToday:
    """
    This function returns the summary of the expenses of a day like today.

    Returns
    -------
    SummaryADayLikeToday
        The summary of the expenses of a day like today.
    """
    # Return the summary
    return SummaryADayLikeToday(
        **get_summary_a_day_like_today(
            datetime.datetime.now()
            .astimezone(pytz.timezone("America/Bogota"))
            .isoweekday()
        )
    )


# Create the endpoint to get all the transactions of the current day
@router.get(
    "/get_full_transactions_day/",
    response_model=List[TransactionInfo],
    dependencies=[Depends(check_access_token)],
)
async def get_full_transactions() -> List[TransactionInfo]:
    """
    This function returns the full transactions of the current day

    Returns
    -------
    List[TransactionInfo]
        The summary of the expenses of the day, week or month.
    """
    return get_gross_transactions("daily")
