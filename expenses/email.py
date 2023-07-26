import os
from datetime import datetime
from email.message import Message
from bs4 import BeautifulSoup

import pytz

from .client import GmailClient


class TransactionEmail:
    def __init__(self, email: Message):
        self.body_email = email
        self._date: datetime = None
        self._str_message: str = None

    def __str__(self) -> str:
        """
        This function returns the transaction message.

        Returns
        -------
        str
            The transaction message.
        """
        return self.str_message

    @property
    def str_message(self) -> str:
        """
        This property obtains the transaction message from the email.

        The logic behind this is the following:
            1. The transaction message is the first line that starts with
                "Bancolombia" in the entire mail.
            2. The message is always splitted in two lines, so we need to
                join the two lines.

        Returns
        -------
        str
            The transaction message.
        """
        if not self._str_message:
            # Get the text of the email
            soup = BeautifulSoup(self.body_email.as_string(), "html.parser")
            text_lines = soup.get_text().replace("=", "").splitlines()

            # This is prone to errors, but it works for now.
            self._str_message = [
                line.strip() + text_lines[i + 1]
                for i, line in enumerate(text_lines)
                if line.strip() and line.strip().startswith("Bancolombia")
            ][0]

            return self._str_message

    @property
    def date(self) -> datetime:
        """
        This property obtains the date when the email was received.
        Notice that this date is obtained from the email itself, not from the
        transaction message, so it could be differences.

        Returns
        -------
        datetime
            The date when the email was received.
        """
        if not self._date:
            # Get the date of the email.
            # Format: "Tue, 25 Jul 2023 01:07:29 +0000 (UTC)"
            datetime_email = self.body_email["Date"]

            # Convert to datetime object
            datetime_email = datetime.strptime(
                datetime_email, "%a, %d %b %Y %H:%M:%S %z (%Z)"
            )

            # The date is given in the UTC. We need UTC-5
            self._date = datetime_email.astimezone(
                pytz.timezone("America/Bogota")
            )
            return self._date


if __name__ == "__main__":
    EMAIL_FROM = "alertasynotificaciones@notificacionesbancolombia.com"

    gmail_client = GmailClient(os.getenv("EMAIL"))
    emails_list = gmail_client.obtain_emails(
        EMAIL_FROM, most_recents_first=True, limit=3
    )
    email_test = emails_list[2]
    transaction_email = TransactionEmail(email_test)
    print(transaction_email.str_message)
