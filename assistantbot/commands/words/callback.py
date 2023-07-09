from telegram import Update
from telegram.ext import ContextTypes

from assistantbot.ai.text.commands.base_response import BaseResponse
from assistantbot.ai.text.prompts.words import (
    RANDOM_WORD_PROMPT_TEMPLATE_DEFINITION,
    RANDOM_WORD_PROMPT_TEMPLATE_WITHOUT_DEFINITION,
    USER_PROMPT_TEMPLATE,
)
from assistantbot.logs.configuration import logger

from .utils import get_random_word


class CallbackRandomWord:
    def __init__(self) -> None:
        """
        This class is used to get the response of the llm based on the random
        word of the day.
        """
        self.word_data = None
        self.prompt_word_template = None

    def _set_random_word(self) -> None:
        """
        This function is used to set the random word of the day and
        the prompt
        """
        # Get the random word of the day
        self.word_data = get_random_word()

        # Get the prompt template
        if self.word_data["definition"]:
            self.prompt_word_template = (
                RANDOM_WORD_PROMPT_TEMPLATE_DEFINITION
            )
        else:
            self.prompt_word_template = (
                RANDOM_WORD_PROMPT_TEMPLATE_WITHOUT_DEFINITION
            )

    async def get_random_word_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Get the response of the llm based on the random word of the day

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

        # Change the word in every response
        self._set_random_word()
        logger.info(
            f"Random word of the day obtained: {self.word_data['word']}"
        )

        # Instantiate the AI response
        get_random_word_response = BaseResponse(
            self.prompt_word_template, USER_PROMPT_TEMPLATE
        ).create_response

        # Get the message to send to the user
        response_word = get_random_word_response(**self.word_data)

        # Send the current temperature to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_word,
        )
