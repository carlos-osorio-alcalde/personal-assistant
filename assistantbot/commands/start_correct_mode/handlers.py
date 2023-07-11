from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from assistantbot.commands.start_correct_mode.callback import (
    entry_correct_grammar,
    correct_grammar,
    state_message,
)
from assistantbot.commands.end_correct_mode.callback import (
    end_correct_grammar,
)


def start_correct_mode_handler() -> CommandHandler:
    """
    This function returns the handler for the correct command.

    Returns
    -------
    CommandHandler
        The command handler.
    """
    return ConversationHandler(
        entry_points=[
            CommandHandler("start_correct_mode", entry_correct_grammar)
        ],
        states={
            state_message: [
                MessageHandler(
                    filters.TEXT & (~filters.COMMAND), correct_grammar
                )
            ]
        },
        fallbacks=[CommandHandler("end_correct_mode", end_correct_grammar)],
    )
