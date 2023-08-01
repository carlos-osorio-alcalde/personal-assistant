from abc import ABC, abstractmethod
from typing import List

from expenses.constants import (
    TRANSACTION_MESSAGES_TYPES_,
    TRANSACTION_TYPES_,
)
from expenses.email import TransactionEmail
from expenses.processors.schemas import TransactionInfo


class EmailProcessor(ABC):
    def __init__(self, email: TransactionEmail):
        self.email = email
        self.transaction_email_text = self.email.str_message
        self.transaction_type = None

    def __str__(self):
        return f"{self.__class__.__name__}"

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

    @staticmethod
    def convert_amount_to_float(value_str: str) -> float:
        """
        This static method converts a string amount to float.
        There are several possible formats for the amount:
            1. 57,000.00
            2. 57.000,00
            3. 57,000
            4. 57.000

        Parameters
        ----------
        value_str : str
            The string amount.

        Returns
        -------
        float
            The float amount.
        """
        # Delete the "$" symbol
        value_str = value_str.replace("$", "")

        # Check if the comma or the dot appears first
        if "," in value_str and "." in value_str:
            if value_str.index(",") < value_str.index("."):
                value_str = value_str.split(".")[0]
            else:
                value_str = value_str.split(",")[0]

        value_str = value_str.replace(",", "").replace(".", "")
        return float(value_str)

    @abstractmethod
    def process(self) -> TransactionInfo:
        """
        This function processes the information of the email. It extracts the
        transaction type, the amount and the merchant.

        Returns
        -------
        TransactionInfo
            The transaction info schema.
        """
        ...


if __name__ == "__main__":
    pass
