from telegram.ext import CommandHandler

from assistantbot.commands.start.callback import start_conversation


# Instantiate the start handler
def start_handler() -> CommandHandler:
    """
    This function returns the start handler.

    Returns
    -------
    CommandHandler
        The start handler.
    """
    return CommandHandler("start", start_conversation)
