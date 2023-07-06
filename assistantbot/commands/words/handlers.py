from telegram.ext import CommandHandler

from assistantbot.commands.words.callback import CallbackRandomWord
from .utils import get_random_word


# Instantiate the start handler
def words_handler() -> CommandHandler:
    """
    This function returns the start handler.

    Returns
    -------
    CommandHandler
        The start handler.
    """
    return CommandHandler(
        "random_word",
        CallbackRandomWord(get_random_word()).get_random_word_response,
    )
