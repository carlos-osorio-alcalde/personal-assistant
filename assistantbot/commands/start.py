import os

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from assistantbot.ai.text.base_response import BaseResponse
from assistantbot.ai.text.prompts.start import (
    START_PROMPT_TEMPLATE,
    START_USER_TEMPLATE,
)
from assistantbot.commands.base import BaseCommand
from assistantbot.utils.time import get_weekday_moment


class StartCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self._command = "start"

    @staticmethod
    async def command_callback(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This function is called when the user sends the /start command.

        The function sends a greeting message to Carlos.

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : ContextTypes.DEFAULT_TYPE
            The context object from Telegram.
        """
        # Instantiate the AI response
        create_start_answer = BaseResponse(
            START_PROMPT_TEMPLATE, START_USER_TEMPLATE
        ).create_response

        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # Check if the sender is the id of Carlos
        start_message = create_start_answer(**get_weekday_moment())

        # Send the start message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=start_message,
        )

    def command_handler(self) -> CommandHandler:
        """
        This function returns the start handler.

        Returns
        -------
        CommandHandler
            The start handler.
        """
        return CommandHandler(self._command, self.command_callback)

    @property
    def command_name(self):
        return self._command
