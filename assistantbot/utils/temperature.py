import json
import os
from pathlib import Path
from typing import Dict, Literal

import requests
from dotenv import load_dotenv

from assistantbot.configuration import config

# Load environment variables
load_dotenv()


def get_configured_locations(raw: bool = True) -> Dict:
    """
    This function returns the configured locations from the locations.json

    Parameters
    ----------
    raw : bool, optional
        If True, return the raw locations, by default True

    Returns
    -------
    Dict
        The configured locations.
    """
    # Load the file locations.json into a dictionary
    path_location_json = Path(config["WEATHER_LOCATIONS"])
    temperature_locations_ = json.load(open(path_location_json))
    temperature_locations = {
        location: values["name"]
        for location, values in temperature_locations_.items()
    }
    return temperature_locations_ if raw else temperature_locations


def is_configured_location(location) -> bool:
    """
    Check if the location is configured in the locations.json file.

    Returns
    -------
    bool
        True if the location is configured, False otherwise.
    """
    return True if location in get_configured_locations(raw=False) else False


def get_weather_conditions(city: Literal["med", "bog", "tul"]) -> Dict:
    """
    This function gets the current temperature in a city.

    Parameters
    ----------
    city : Literal['med', 'bog', 'tul']
        The city to get the temperature from.

    Returns
    -------
    str
        The current temperature in the city.
    """
    temperature_locations_ = get_configured_locations(raw=True)

    # Get the current temperature
    url = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat={lat}&lon={lon}&units=metric&appid={api_key}"
    )
    response = requests.get(
        url.format(
            lat=temperature_locations_[city]["lat"],
            lon=temperature_locations_[city]["lon"],
            api_key=os.getenv("OPEN_WEATHER_API_KEY"),
        ),
        timeout=config["TIMEOUT"],
    )

    if response.status_code != 200:
        return {
            "location": "",
            "temperature": "",
            "weather_status": "",
        }

    return {
        "location": temperature_locations_[city],
        "temperature": response.json()["main"]["temp"],
        "weather_status": response.json()["weather"][0]["description"],
    }
