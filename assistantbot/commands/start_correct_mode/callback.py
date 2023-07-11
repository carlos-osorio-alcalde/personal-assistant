from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes


# This variable will store the message to correct
state_message = ""


async def entry_correct_grammar(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    This function corrects the grammar of the message sent by the user.

    Parameters
    ----------
    update : telegram.Update
        The update object.
    context : telegram.ext.CallbackContext
        The callback context.
    """
    entry_message = """
    Hey Carlos! Send me a message to correct your grammar.
    I pledge to not make a lot of changes.
    """

    # First, the bot sends the option to write the message to correct
    await update.message.reply_text(
        entry_message, reply_markup=ReplyKeyboardRemove()
    )

    return state_message


async def correct_grammar(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This function corrects the grammar of the message sent by the user.

    Parameters
    ----------
    update : telegram.Update
        The update object.
    context : telegram.ext.CallbackContext
        The callback context.
    """
    # Get the message to correct
    message = update.effective_message.text

    # TODO: Implement the AI corrector, for now, the bot will send the same
    corrected_message = message

    # The bot sends the message to correct
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=corrected_message,
    )
