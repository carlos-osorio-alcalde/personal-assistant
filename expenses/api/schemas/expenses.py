import datetime

from pydantic import BaseModel

from expenses.processors.schemas import TransactionInfo


class BaseTransactionInfo(BaseModel):
    """
    This class represents the base of the transaction info.
    """

    name: str | None
    amount: float | None
    count: int | None


class SummaryTransactionInfo(BaseModel):
    """
    This class represents the summary of all the transactions of the
    day, week or month.
    """

    purchases: BaseTransactionInfo
    withdrawals: BaseTransactionInfo
    transfer_reception: BaseTransactionInfo
    transfer_qr: BaseTransactionInfo
    payment: BaseTransactionInfo
    transfer: BaseTransactionInfo


class AddTransactionInfo(TransactionInfo):
    """
    This class is used to add a transaction manually.
    This inherits from TransactionInfo.
    """

    datetime = datetime.datetime.now()
    paynment_method: str = "Cash"
    email_log: str = ""
