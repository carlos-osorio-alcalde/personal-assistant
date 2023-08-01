import re

from expenses.email import TransactionEmail
from expenses.processors.base import EmailProcessor
from expenses.processors.schemas import TransactionInfo


class PurchaseEmailProcessor(EmailProcessor):
    def __init__(self, email: TransactionEmail):
        super().__init__(email)
        self.type_transaction = "Compra"

    def process(self) -> TransactionInfo:
        """
        This function processes the information of the email. It extracts the
        transaction type, the amount and the merchant.

        Returns
        -------
        TransactionInfo
            The transaction information.
        """
        if not self._is_valid_email():
            return None, None, None

        pattern = (
            r"Compra por (?P<purchase_amount>.*?) en (?P<merchant>.*?)"
            r"(?: (?P<time>\d{2}:\d{2}). (?P<date>\d{2}/\d{2}/\d{4}))?"
            r" (?P<payment_method>T.(?:Cred|Deb) \*\d+)."
        )
        match = re.search(pattern, self.transaction_email_text)
        if match:
            purchase_amount = match.group("purchase_amount")
            merchant = match.group("merchant")
            paynment_method = match.group("payment_method")

        return TransactionInfo(
            transaction_type=self.type_transaction,
            amount=self.convert_amount_to_float(purchase_amount),
            merchant=merchant,
            datetime=self.email.date_message,
            paynment_method=paynment_method,
        )
