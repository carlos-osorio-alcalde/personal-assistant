import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from assistantbot.commands import (
    end_correct_mode,
    start,
    start_correct_mode,
    temperature,
    words,
)

# from assistantbot.commands_handlers import get_implemented_command_handlers
from assistantbot.configuration import config
from assistantbot.conversation.text.handlers import message_handler
from assistantbot.error_handler import error_handler
from assistantbot.logs.configuration import logger

# Load environment variables
load_dotenv()


def main() -> None:
    """
    This function starts the bot.
    """
    # Get the bot token from the environment variables
    app = (
        ApplicationBuilder()
        .token(os.getenv("BOT_TOKEN_KEY"))
        .connect_timeout(config["TIMEOUT"])
        .get_updates_connect_timeout(config["TIMEOUT"])
        .pool_timeout(config["TIMEOUT"])
        .build()
    )
    logger.info("Bot started")

    # Add the handlers
    app.add_handler(start.StartCommand().command_handler())
    app.add_handler(words.WordsCommand().command_handler())
    app.add_handler(
        start_correct_mode.StartCorrectModeCommand().command_handler()
    )
    app.add_handler(
        end_correct_mode.EndCorrectModeCommand().command_handler()
    )
    # For temperature, create the handlers
    temperature_handlers = (
        temperature.TemperatureCommandFactory().create_handlers()
    )
    for handler in temperature_handlers:
        app.add_handler(handler.command_handler())

    # Add the message handler
    app.add_handler(message_handler())

    # Add the error handler
    app.add_error_handler(error_handler)

    # Run the bot
    app.run_polling(
        timeout=config["TIMEOUT"],
        allowed_updates=config["ALLOWED_UPDATES"],
        connect_timeout=config["TIMEOUT"],
    )
