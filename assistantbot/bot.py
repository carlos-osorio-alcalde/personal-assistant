import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from assistantbot.commands import temperature
from assistantbot.commands_handlers import get_implemented_command_handlers
from assistantbot.configuration import config
from assistantbot.conversation.text.handlers import TextHandler
from assistantbot.conversation.voice.handlers import VoiceHandler
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

    # Add the implemented command handlers
    for handler in get_implemented_command_handlers():
        app.add_handler(handler().command_handler())

    # For temperature, create the handlers using the factory
    temperature_handlers = (
        temperature.TemperatureCommandFactory().create_handlers()
    )
    for handler in temperature_handlers:
        app.add_handler(handler.command_handler())

    # Add the message handler
    text_handler = TextHandler()
    app.add_handler(text_handler.handler())

    # Add the voice handler
    app.add_handler(
        VoiceHandler(
            conversation_chain=text_handler.conversation_chain
        ).handler()
    )

    # Add the error handler
    app.add_error_handler(error_handler)

    # Run the bot
    app.run_polling(
        timeout=config["TIMEOUT"],
        allowed_updates=config["ALLOWED_UPDATES"],
        connect_timeout=config["TIMEOUT"],
    )
