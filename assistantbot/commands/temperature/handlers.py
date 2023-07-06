import json
from pathlib import Path
from typing import List

from telegram.ext import CommandHandler

from assistantbot.commands.temperature.callback import CallbackTemperature


def temperature_handler() -> List[CommandHandler]:
    """
    This function returns the temperature handlers for each configured
    location.

    Returns
    -------
    List[CommandHandler]
        List of temperature handlers.
    """
    # Load the file locations.json into a dictionary
    path_location_json = Path(
        "assistantbot/commands/temperature/locations.json"
    )
    temperature_locations_ = json.load(open(path_location_json))
    temperature_locations = {
        location: values["name"]
        for location, values in temperature_locations_.items()
    }

    temperature_handlers = []
    for location in temperature_locations:
        # Add the temperature handler for each location
        temperature_handlers.append(
            CommandHandler(
                f"temperature_{location}",
                CallbackTemperature(location).get_temperature_response,
            )
        )

    return temperature_handlers
