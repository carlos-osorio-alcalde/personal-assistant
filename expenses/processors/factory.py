from expenses.constants import TRANSACTION_TYPES_
import expenses.processors.transactions as transactions_processors
from expenses.email import TransactionEmail
from expenses.processors.base import EmailProcessor

# Transaction types and their corresponding processors
TRANSACTIONS_PROCESSORS_ = {
    "Compra": transactions_processors.PurchaseEmailProcessor,
    "Recepcion transferencia": transactions_processors.TransferEmailProcessor,
}


class EmailProcessorFactory:
    """
    This class is the factory of the email processors. It identifies the
    transaction type of the email and returns the corresponding processor.
    """

    @staticmethod
    def _identify_transaction_type(email: TransactionEmail) -> str:
        """
        This function identifies the transaction type of the email. It checks
        if the email contains a valid transaction type.

        Returns
        -------
        str
            The transaction type.
        """
        str_message_lower = email.str_message.lower()
        for transaction_type in TRANSACTION_TYPES_:
            if transaction_type.lower() in str_message_lower:
                return transaction_type

    def get_processor(self, email: TransactionEmail) -> EmailProcessor:
        """
        This function returns the processor of the email.

        Returns
        -------
        BaseEmailProcessor
            The email processor.
        """
        transaction_type = self._identify_transaction_type(email)

        if transaction_type in TRANSACTIONS_PROCESSORS_:
            return TRANSACTIONS_PROCESSORS_[transaction_type](email)
        else:
            raise ValueError(
                f"The transaction type {transaction_type} is not supported."
            )
