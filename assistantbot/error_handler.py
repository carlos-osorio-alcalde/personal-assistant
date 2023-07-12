from telegram import Update
from telegram.ext import ContextTypes

from assistantbot.configuration import config


async def error_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This function is called when an error occurs and sends a message

    Parameters
    ----------
    update : Update
        The update object from Telegram.
    context : ContextTypes.DEFAULT_TYPE
        The context object from Telegram.
    """
    # Get the last error from logs/assistantbot.log
    with open(config["ERROR_LOG_FILE"], "r") as f:
        lines = f.readlines()
        last_line_error = lines[-1].strip()

    # Get the message from the error
    message = f"""
        Something went wrong. This is the last line from the error log.
        Please, Carlos, check the error log file and fix the error.
        The last line from the error log is:

        {last_line_error}
    """

    # Send the error message to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
    )
