from pydantic import BaseModel


class TransactionInfo(BaseModel):
    transaction_type: str
    amount: float
    merchant: str | None
    time: str
    date: str
    paynment_method: str | None
