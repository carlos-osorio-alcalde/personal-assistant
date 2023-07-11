from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def end_correct_grammar(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> ConversationHandler.END:
    """
    This function is the callback to end the correct grammar mode.

    Parameters
    ----------
    update : Update
        The update object.
    context : ContextTypes.DEFAULT_TYPE
        The callback context.

    Returns
    -------
    ConversationHandler.END
        The end of the conversation.
    """
    # Message to end the conversation
    final_message = "Ok, Carlos! You will return to the normal mode."

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=final_message,
    )

    return ConversationHandler.END
