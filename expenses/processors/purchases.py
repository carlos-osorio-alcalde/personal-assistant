import re
from expenses.processors.base import BaseEmailProcessor
from expenses.processors.schemas import TransactionInfo


class PurchasesEmailProcessor(BaseEmailProcessor):
    def __init__(self, email):
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
            r"Compra por (.*?) en (.*?)(?: (\d{2}:\d{2})."
            r" (\d{2}/\d{2}/\d{4}))? (T.(?:Cred|Deb) \*\d+)."
        )
        match = re.search(pattern, self.transaction_email_text)
        if match:
            purchase_amount = match.group(1)
            merchant = match.group(2)
            time = match.group(3)
            date = match.group(4)
            paynment_method = match.group(5)

        return TransactionInfo(
            transaction_type=self.type_transaction,
            amount=self.convert_amount_to_float(purchase_amount),
            merchant=merchant,
            time=time,
            date=date,
            paynment_method=paynment_method,
        )


if __name__ == "__main__":
    from expenses.email import TransactionEmail
    from expenses.client import GmailClient
    import os

    EMAIL_FROM = "alertasynotificaciones@notificacionesbancolombia.com"

    gmail_client = GmailClient(os.getenv("EMAIL"))
    emails_list = gmail_client.obtain_emails(
        EMAIL_FROM, most_recents_first=True, limit=3
    )
    email_test = emails_list[0]
    transaction_email = TransactionEmail(email_test)
    processor = PurchasesEmailProcessor(transaction_email)
    print(processor.process())
