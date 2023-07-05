import json
import os
from pathlib import Path
from typing import Literal

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_weather_conditions(city: Literal["med", "bog", "tul"]):
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
    # Locations of the cities
    PATH_LOCATIONS = Path(__file__).parent / "locations.json"
    locations = json.load(open(PATH_LOCATIONS))

    # Get the current temperature
    url = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat={lat}&lon={lon}&units=metric&appid={api_key}"
    )
    response = requests.get(
        url.format(
            lat=locations[city]["lat"],
            lon=locations[city]["lon"],
            api_key=os.getenv("OPEN_WEATHER_API"),
        )
    )

    if response.status_code != 200:
        return {
            "location": "",
            "temperature": "",
            "weather_status": "",
        }

    return {
        "location": locations[city],
        "temperature": response.json()["main"]["temp"],
        "weather_status": response.json()["weather"][0]["description"],
    }


if __name__ == "__main__":
    print(get_weather_conditions("med"))
