from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from assistantbot.ai.text.commands.base_response import BaseResponse
from assistantbot.ai.text.prompts.temperature import (
    TEMPERATURE_PROMPT_TEMPLATE,
    USER_PROMPT_TEMPLATE,
)

from .utils import get_weather_conditions


class CallbackTemperature:
    """
    This class is the callback for the the /temperature command.
    """

    def __init__(self, location: Optional[str] = None) -> None:
        """
        This function initializes the class.

        Parameters
        ----------
        location : Optional[str]
            The location to get the temperature from.
        """
        self.location = location

    async def get_temperature_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This function is called when the user sends the /temperature command.

        The function sends the current temperature in the location.

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
        get_weather_response = BaseResponse(
            TEMPERATURE_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE
        ).create_response

        # Get the message to send to the user
        weather_response = get_weather_response(
            **get_weather_conditions(self.location)
        )

        # Send the current temperature to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=weather_response,
        )
