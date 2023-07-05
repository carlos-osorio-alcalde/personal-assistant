import datetime
from typing import Dict


def get_weekday_moment() -> Dict:
    """
    This function checks the day of the week and the moment
    of the day

    Returns
    -------
    Dict
        The dictionary with day and hour of the day
    """
    now = datetime.datetime.now()
    hour = now.hour
    if 0 <= hour < 12:
        moment = "morning"
    elif 12 <= hour < 18:
        moment = "afternoon"
    else:
        moment = "evening"
    date = now.date()

    return {
        "date": now.date().strftime("%Y-%m-%d"),
        "moment": moment,
        "day": date.strftime("%A"),
    }
