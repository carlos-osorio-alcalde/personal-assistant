from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.conversation.base import ConversationHandler
from assistantbot.conversation.chains import (
    get_conversation_chain,
    update_memory,
)


class TextHandler(ConversationHandler):
    def __init__(self):
        super().__init__(filters.TEXT)

    def handler(self) -> MessageHandler:
        """
        This function returns the message handler.

        Returns
        -------
        MessageHandler
            The message handler.
        """
        return MessageHandler(self._type, self.callback, block=False)

    async def callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        This function is called when a text message is sent to the bot.

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : _type_
            The context object from Telegram.
        """
        # Get the message text
        response_message = """
🚀 Hey there, folks! 
We're moving to @lingolearn_bot for an even better English learning experience! 
While this direction will no longer be available, rest assured that everything remains the same, just in a new direction.
See you there! 🌟📚😊
"""

        # Send the start message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message,
        )
