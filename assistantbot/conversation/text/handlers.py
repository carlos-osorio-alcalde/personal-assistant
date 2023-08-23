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
        # Get the conversation chain
        conversation_chain = get_conversation_chain(update.effective_user.id)

        # Get the input message
        entry_message = update.effective_message.text

        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_user.id, action="typing"
        )

        # Predict the response
        try:
            response_message = await conversation_chain.apredict(
                input=entry_message
            )
        except Exception:
            # Clear the memory if the conversation is too long
            conversation_chain.memory.clear()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Well, we've had a very long conversation. \
                    I will forget everything we've talked about to \
                    be able to continue our conversation.",
            )
            response_message = await conversation_chain.apredict(
                input=entry_message
            )

        # Update the memory
        update_memory(update.effective_user.id, conversation_chain)

        # Send the start message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message,
        )
