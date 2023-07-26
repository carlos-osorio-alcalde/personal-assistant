from .email import TransactionEmail
from typing import List, Tuple
import re

TRANSACTION_MESSAGES_TYPES_ = [
    "Bancolombia le informa",
    "Bancolombia te informa",
    "Bancolombia informa",
]

TRANSACTION_TYPES_ = [
    "Compra",
    "Retiro",
    "Pago",
    "Recepcion transferencia",
    "Retiro",
]


class TransactionEmailProcessor:
    def __init__(self, email: TransactionEmail):
        self.transaction_email_text = email.str_message

    @staticmethod
    def _has_valid_messages(messages: List[str], email_text: str) -> bool:
        """
        This static method checks if the email contains some of the messages
        in the list.

        Parameters
        ----------
        messages : List[str]
            The list of messages to check.
        email_text : str
            The email text.

        Returns
        -------
        bool
            True if the email contains some of the messages, False otherwise.
        """
        return any(message in email_text for message in messages)

    def _is_valid_email(self) -> bool:
        """
        This function checks if the email is valid. For that, it must
        contain the following:
            1. The email must be from Bancolombia.
            2. The email must contain the transaction message.
            3. The email must contain the transaction date.
            4. The email must contain the transaction amount.

        Returns
        -------
        bool
            True if the email is valid, False otherwise.
        """
        # Check if the string email contains some of the messages types
        has_valid_message_type = self._has_valid_messages(
            TRANSACTION_MESSAGES_TYPES_, self.transaction_email_text
        )

        # Check if the string email contains some of the transaction types
        has_valid_transaction_type = self._has_valid_messages(
            TRANSACTION_TYPES_, self.transaction_email_text
        )

        # Check if the string email contains an amount with "$"
        has_valid_amount = "$" in self.transaction_email_text

        # Return True if all conditions are met, otherwise False
        return (
            has_valid_message_type
            and has_valid_transaction_type
            and has_valid_amount
        )

    def process_information(self) -> Tuple[str, str, str]:
        """
        This function processes the information of the email. It extracts the
        transaction type, the amount and the merchant.

        Returns
        -------
        Tuple[str, str, str]
            The transaction type, the amount and the merchant.
        """
        if not self._is_valid_email():
            return None, None, None

        # Regular expressions for different parts of the transaction string
        # using the TRANSACTION_TYPES_
        transaction_type_pattern = r"(?:{})".format(
            "|".join(TRANSACTION_TYPES_)
        )
        amount_pattern = r"\$[\d,]+(?:\.\d+)?"
        merchant_pattern = r"(?:\*[\d]+|[\w/.]+)"  # This is not correct.

        # Extract transaction type
        transaction_type_match = re.search(
            transaction_type_pattern,
            self.transaction_email_text,
            re.IGNORECASE,
        )
        transaction_type = (
            transaction_type_match.group(0).lower()
            if transaction_type_match
            else None
        )

        # Extract amount
        amount_match = re.search(amount_pattern, self.transaction_email_text)
        amount = amount_match.group(0) if amount_match else None

        # Extract merchant
        merchant_match = re.search(
            merchant_pattern, self.transaction_email_text, re.IGNORECASE
        )
        merchant = merchant_match.group(0) if merchant_match else None

        return transaction_type, amount, merchant


if __name__ == "__main__":
    pass
