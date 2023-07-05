from typing import Optional

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from telegram import Update
from telegram.ext import ContextTypes

from assistantbot.ai.text.llm import chat_llm


class ConversationCallback:
    def __init__(
        self, base_system_prompt: str, llm: Optional[ChatOpenAI] = chat_llm
    ):
        """
        This object handles the usual conversational commands.

        Parameters
        ----------
        base_system_prompt : str
            Base system prompt for the conversation.
        llm : Optional[ChatOpenAI], optional
            The llm to use, by default chat_llm
        """
        self.chat_llm = llm

        PROMPT = PromptTemplate(
            input_variables=["history", "input"], template=base_system_prompt
        )

        self.conversation_chain = ConversationChain(
            prompt=PROMPT,
            llm=self.chat_llm,
            verbose=False,
            memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
        )

    async def create_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> str:
        """
        This function creates a response to the input using the
        conversation chain. It returns the response.

        Parameters
        ----------
        input : str
            Text input to the conversation chain.

        Returns
        -------
        str
            Response of the conversation chain.
        """
        # Get the input message
        entry_message = update.effective_message.text

        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # Predict the response
        response_message = self.conversation_chain.predict(
            input=entry_message
        )

        # Send the start message to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message,
        )
