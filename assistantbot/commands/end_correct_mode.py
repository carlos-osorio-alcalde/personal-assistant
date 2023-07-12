from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from assistantbot.commands.base import BaseCommand


class EndCorrectModeCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command = "end_correct_mode"

    @staticmethod
    async def command_callback(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationHandler.END:
        """
        This function is the callback to end the correct grammar mode.

        Parameters
        ----------
        update : Update
            The update object.
        context : ContextTypes.DEFAULT_TYPE
            The callback context.

        Returns
        -------
        ConversationHandler.END
            The end of the conversation.
        """
        # Message to end the conversation
        final_message = "Ok, Carlos! You will return to the normal mode."

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=final_message,
        )

        return ConversationHandler.END

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
