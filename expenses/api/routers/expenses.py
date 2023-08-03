from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from expenses.api.schemas.expenses import SummaryTransactionInfo
from expenses.api.security import check_access_token
from expenses.api.utils import (
    get_date_from_search,
    get_transactions,
    process_transactions_api,
)

router = APIRouter(prefix="/expenses")


# Create the router
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
    # Check if the timeframe is valid
    if timeframe not in ["daily", "weekly", "partial_weekly", "monthly"]:
        raise HTTPException(
            status_code=400,
            detail="The timeframe must be daily, weekly, partial_weekly or "
            "monthly",
        )

    # Get the date to search
    date_to_search = get_date_from_search(timeframe)

    # Process the transactions
    transactions = get_transactions(date_to_search)

    return process_transactions_api(transactions)
