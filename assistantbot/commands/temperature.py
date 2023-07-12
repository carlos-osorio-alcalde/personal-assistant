from typing import List, Optional

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from assistantbot.ai.text.commands.base_response import BaseResponse
from assistantbot.ai.text.prompts.temperature import (
    TEMPERATURE_PROMPT_TEMPLATE,
    USER_PROMPT_TEMPLATE,
)
from assistantbot.commands.base import BaseCommand
from assistantbot.utils.temperature import (
    get_configured_locations,
    get_weather_conditions,
    is_configured_location,
)


class TemperatureCommand(BaseCommand):
    """
    This class implements the /temperature for a specific location.
    """

    def __init__(self, location: str):
        super().__init__()
        self._command = f"temperature_{location}"
        self._location = (
            location if is_configured_location(location) else "mde"
        )

    async def command_callback(
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
            **get_weather_conditions(self._location)
        )

        # Send the current temperature to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=weather_response,
        )

    def command_handler(self) -> CommandHandler:
        """
        This function returns the temperature handlers for each configured
        location.

        Returns
        -------
        List[CommandHandler]
            List of temperature handlers.
        """
        return CommandHandler(self._command, self.command_callback)


class TemperatureCommandFactory:
    """
    This class implements the /temperature command factory for each
    configured location.
    """

    def __init__(self, locations: Optional[List[str]] = None):
        self._locations = (
            get_configured_locations() if locations is None else locations
        )

    def create_handlers(self) -> List[TemperatureCommand]:
        """
        This function returns the temperature handlers for each configured
        location.

        Returns
        -------
        List[CommandHandler]
            List of temperature handlers.
        """
        return [
            TemperatureCommand(location)
            for location in self._locations
            if is_configured_location(location)
        ]
