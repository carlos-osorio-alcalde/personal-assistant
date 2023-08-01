import datetime

from pydantic import BaseModel


class TransactionInfo(BaseModel):
    transaction_type: str
    amount: float
    merchant: str | None
    datetime: datetime.datetime
    paynment_method: str | None
