from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from assistantbot.commands.base import BaseCommand
from assistantbot.utils.expenses import get_expenses


class GetDailyExpensesCommand(BaseCommand):
    """
    This class is the command that gets the daily expenses.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_daily_expenses"

    async def command_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Get the daily expenses.

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : ContextTypes.DEFAULT_TYPE
            The context object from Telegram.
        """
        # Send a message telling the user this process could take a while
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This process could take a while ⏳",
        )

        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # Get the expenses
        expenses = get_expenses("daily")

        # Send the message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=expenses,
        )

    # Instantiate the start handler
    def command_handler(self) -> CommandHandler:
        """
        This function returns the start handler.

        Returns
        -------
        CommandHandler
            The start handler.
        """
        return CommandHandler(self._command, self.command_callback)
