import imaplib
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GmailClient:
    def __init__(self, email):
        self._email = email
        self.conn = imaplib.IMAP4_SSL("imap.gmail.com")

    def _connect(self, token: str) -> None:
        """
        This function connects to the IMAP server using the provided token.

        Parameters
        ----------
        token : str
            The app token generated by Gmail.

        Returns
        -------
        imaplib.IMAP4_SSL or None
            The connection to the IMAP server. If the connection fails, None
        """
        try:
            self.conn.login(os.getenv("EMAIL"), token)
        except imaplib.IMAP4.error as e:
            print(f"Error connecting to IMAP server: {e}")

    def _obtain_emails_ids(
        self, email_from: str, most_recents_first: True
    ) -> List[str]:
        """
        This function obtains the ids of the emails from the specified email
        address.

        Parameters
        ----------
        email_from : str
            The email address to obtain the emails from.

        most_recents_first: bool
            If True, obtain the most recent email. If False, obtain the
            messages from the beginning.

        Returns
        -------
        List[str]
            The ids of the emails from the specified email address.
        """
        if self.conn is None:
            self._connect(os.getenv("GMAIL_TOKEN"))

        self.conn.select("Inbox")
        _, msgs_ids = self.conn.search(None, "FROM", f'"{email_from}"')

        # The msgs ids are returned as a list of bytes, so we need to decode
        # them to strings
        msgs_ids = [msg_id.decode("utf-8") for msg_id in msgs_ids[0].split()]

        if most_recents_first:
            msgs_ids.reverse()

        return msgs_ids

    def obtain_emails(
        self, email_from: str, most_recents_first: True, limit: int = None
    ) -> List:
        """
        This function obtains the emails from the specified email address.

        Parameters
        ----------
        email_from : str
            The email address to obtain the emails from.

        most_recents_first: bool
            If True, obtain the most recent email. If False, obtain the
            messages from the beginning.

        limit: int, optional
            The maximum number of emails to obtain. If None, obtain all the
            emails.

        Returns
        -------
        List
            The emails from the specified email address.
        """
        if self.conn is None:
            self._connect(os.getenv("GMAIL_TOKEN"))

        msgs_ids = self._obtain_emails_ids(email_from, most_recents_first)
        limit = len(msgs_ids) if limit is None else limit
        msgs = [
            self.conn.fetch(msg_id, "(RFC822)")[1][0][1].decode("utf-8")
            for msg_id in msgs_ids[:limit]
        ]
        return msgs


if __name__ == "__main__":
    EMAIL_FROM = "alertasynotificaciones@notificacionesbancolombia.com"

    gmail_client = GmailClient(os.getenv("EMAIL"))
    gmail_client._connect(os.getenv("GMAIL_TOKEN"))
    print(
        gmail_client.obtain_emails(
            EMAIL_FROM, most_recents_first=True, limit=3
        )
    )
