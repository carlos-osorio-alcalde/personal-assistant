from .client import GmailClient
import os
from datetime import datetime
import pytz
from email.message import Message


class TransactionEmail:
    def __init__(self, email: Message):
        self.body_email = email

    def __str__(self) -> str:
        return "Email"

    def get_received_date(self) -> datetime:
        """
        This function obtains the date when the email was received.

        Returns
        -------
        datetime
            The date when the email was received.
        """
        # Get the date of the email.
        # Format: "Tue, 25 Jul 2023 01:07:29 +0000 (UTC)"
        datetime_email = self.body_email["Date"]

        # Convert to datetime object
        datetime_email = datetime.strptime(
            datetime_email, "%a, %d %b %Y %H:%M:%S %z (%Z)"
        )

        # The date is given in the UTC. We need UTC-5
        datetime_normalized = datetime_email.astimezone(
            pytz.timezone("America/Bogota")
        )
        return datetime_normalized


if __name__ == "__main__":
    EMAIL_FROM = "alertasynotificaciones@notificacionesbancolombia.com"

    gmail_client = GmailClient(os.getenv("EMAIL"))
    emails_list = gmail_client.obtain_emails(
        EMAIL_FROM, most_recents_first=True, limit=3
    )
    email = TransactionEmail(emails_list[0])
