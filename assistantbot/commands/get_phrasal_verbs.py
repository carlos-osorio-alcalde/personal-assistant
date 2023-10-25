from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from assistantbot.ai.text.base_response import BaseResponse
from assistantbot.ai.text.prompts.phrasal import (
    PHRASAL_VERBS_PROMPT_TEMPLATE_DEFINITION,
    USER_PROMPT_TEMPLATE,
)
from assistantbot.commands.base import BaseCommand


class GetPhrasalVerbsCommand(BaseCommand):
    """
    This class implements the /get_phrasal_verbs command.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_phrasal_verbs"

    async def command_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Get a phrasal verb from the LLM and send it to the user

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : ContextTypes.DEFAULT_TYPE
            The context object from Telegram.
        """
        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # Instantiate the AI response
        get_random_word_response = BaseResponse(
            PHRASAL_VERBS_PROMPT_TEMPLATE_DEFINITION, USER_PROMPT_TEMPLATE
        ).create_response

        # Get the message to send to the user
        response_phrasal = get_random_word_response()

        # Send the current temperature to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_phrasal,
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
