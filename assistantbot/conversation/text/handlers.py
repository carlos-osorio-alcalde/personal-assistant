from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.ai.text.llm import chat_llm
from assistantbot.ai.text.prompts.conversation import (
    CONVERSATION_BASE_TEMPLATE,
)
from assistantbot.conversation.base import ConversationHandler
from assistantbot.utils.security import allowed_user_only


class TextHandler(ConversationHandler):
    def __init__(self):
        super().__init__(filters.TEXT)
        self.chat_llm = chat_llm
        PROMPT = PromptTemplate(
            input_variables=["history", "input"],
            template=CONVERSATION_BASE_TEMPLATE,
        )
        self.conversation_chain = ConversationChain(
            prompt=PROMPT,
            llm=self.chat_llm,
            verbose=False,
            memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
        )

    def handler(self) -> MessageHandler:
        """
        This function returns the message handler.

        Returns
        -------
        MessageHandler
            The message handler.
        """
        return MessageHandler(self._type, self.callback, block=False)

    @allowed_user_only
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
        # Get the input message
        entry_message = update.effective_message.text

        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # Predict the response
        try:
            response_message = await self.conversation_chain.apredict(
                input=entry_message
            )
        except Exception:
            # Clear the memory if the conversation is too long
            self.conversation_chain.memory.clear()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Well, we've had a very long conversation. \
                    I will forget everything we've talked about to \
                    be able to continue our conversation.",
            )
            response_message = await self.conversation_chain.apredict(
                input=entry_message
            )

        # Send the start message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message,
        )
