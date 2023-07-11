from telegram.ext import CommandHandler

from assistantbot.commands.end_correct_mode.callback import (
    end_correct_grammar,
)


# Instantiate the start handler
def end_correct_mode_handler() -> CommandHandler:
    """
    This function returns the start handler.

    Returns
    -------
    CommandHandler
        The start handler.
    """
    return CommandHandler("end_correct_mode", end_correct_grammar)
