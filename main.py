import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from assistantbot.configuration_logs import logger
from assistantbot.commands.start.handlers import start_handler
from assistantbot.commands.temperature.handlers import temperature_handlers
from assistantbot.conversation.text.handlers import message_handler

# Load environment variables
load_dotenv()


def main_bot() -> None:
    """
    This function starts the bot.
    """
    # Get the bot token from the environment variables
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    logger.info("Bot started")

    # Add the start handler
    app.add_handler(start_handler())

    # Add the temperature handlers
    for handler in temperature_handlers():
        app.add_handler(handler)

    # Add the message handler
    app.add_handler(message_handler())

    # Run the bot
    app.run_polling()


if __name__ == "__main__":
    main_bot()
