from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from typing import Literal

from assistantbot.ai.text.base_response import BaseResponse
from assistantbot.ai.text.prompts.expenses import (
    EXPENSES_PROMPT_TEMPLATE,
    USER_PROMPT_TEMPLATE_EXPENSES,
)
from assistantbot.commands.base import BaseCommand
from assistantbot.utils.expenses import get_expenses


class GetExpensesCommand(BaseCommand):
    """
    This is the base command to get the expenses from a timeframe.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_daily_expenses"
        self._timeframe: Literal[
            "daily", "weekly", "partial_weekly", "monthly"
        ] = None
        self._median_amount_purchases = 0
        self._mean_num_purchases = 0

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
        expenses_str = get_expenses(self._timeframe)

        # Instantiate the AI response
        get_expenses_response = BaseResponse(
            EXPENSES_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE_EXPENSES  # noqa
        ).create_response

        # Send the message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_expenses_response(
                timeframe=self._timeframe,
                expenses=expenses_str,
                median_amount_purchases=self._median_amount_purchases,
                mean_num_purchases=self._mean_num_purchases,
            ),
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
