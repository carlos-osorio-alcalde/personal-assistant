from abc import ABC, abstractmethod
import re
from expenses.email import TransactionEmail
from expenses.processors.schemas import TransactionInfo
from expenses.processors.constants import (
    TRANSACTION_MESSAGES_TYPES_,
    TRANSACTION_TYPES_,
)
from typing import List


class BaseEmailProcessor(ABC):
    def __init__(self, email: TransactionEmail):
        self.transaction_email_text = email.str_message
        self.transaction_type = None

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

        Parameters
        ----------
        value_str : str
            The string amount.

        Returns
        -------
        float
            The float amount.
        """
        value_str = "".join(
            char for char in value_str if char.isdigit() or char in ",."
        )

        # TODO: Implement a better way to convert the amount to float
        pass

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
