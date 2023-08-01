import re

from expenses.email import TransactionEmail
from expenses.processors.base import EmailProcessor
from expenses.processors.schemas import TransactionInfo


class TransferEmailProcessor(EmailProcessor):
    def __init__(self, email: TransactionEmail):
        super().__init__(email)
        self.type_transaction = "Transferencia"

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

        pattern = re.compile(
            r"recepcion transferencia de (?P<recipient>.*?) "
            r"por (?P<amount>\$\d{1,3}(?:,\d{3})*\.\d{2}) "
            r"en la cuenta \*(?P<account>\d{4}). "
            r"(?P<datetime>\d{2}/\d{2}/\d{4} \d{2}:\d{2})."
        )
        match = pattern.search(self.transaction_email_text)
        if match:
            sender = match.group("recipient")
            transfer_amount = match.group("amount")
            account = match.group("account")

        return TransactionInfo(
            transaction_type=self.type_transaction,
            amount=self.convert_amount_to_float(transfer_amount),
            merchant=sender,
            datetime=self.email.date_message,
            paynment_method=account,
        )
