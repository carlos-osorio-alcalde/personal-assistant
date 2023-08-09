from pydantic import BaseModel


class BaseTransactionInfo(BaseModel):
    """
    This class represents the base of the transaction info.
    """

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
