import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from assistantbot.configuration import config
from assistantbot.logs.configuration import logger
from assistantbot.commands_handlers import get_implemented_command_handlers
from assistantbot.conversation.text.handlers import message_handler
from assistantbot.error_handler import error_handler

# Load environment variables
load_dotenv()


def main_bot() -> None:
    """
    This function starts the bot.
    """
    # Get the bot token from the environment variables
    token = os.getenv("BOT_TOKEN_KEY")
    app = (
        ApplicationBuilder()
        .token(token)
        .connect_timeout(config["TIMEOUT"])
        .get_updates_connect_timeout(config["TIMEOUT"])
        .build()
    )
    logger.info("Bot started")

    # Get the command handlers and add them to the bot
    command_handlers = get_implemented_command_handlers()
    for handler in command_handlers:
        # If the handler returns a list of handlers, add them all
        if isinstance(handler(), list):
            for h in handler():
                app.add_handler(h)
        else:
            app.add_handler(handler())

    # Add the message handler
    app.add_handler(message_handler())

    # Add the error handler
    app.add_error_handler(error_handler)

    # Run the bot
    app.run_polling()


if __name__ == "__main__":
    main_bot()
