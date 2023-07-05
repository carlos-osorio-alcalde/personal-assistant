import os

from telegram import Update
from telegram.ext import ContextTypes

from assistantbot.ai.text.commands.base_response import BaseResponse
from assistantbot.ai.text.prompts.start import (
    START_PROMPT_TEMPLATE,
    START_USER_TEMPLATE,
)

from .utils import get_weekday_moment


async def start_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This function is called when the user sends the /start command.

    The function sends a greeting message to Carlos.

    Parameters
    ----------
    update : Update
        The update object from Telegram.
    context : ContextTypes.DEFAULT_TYPE
        The context object from Telegram.
    """
    # Instantiate the AI response
    create_start_answer = BaseResponse(
        START_PROMPT_TEMPLATE, START_USER_TEMPLATE
    ).create_response

    # Send the typing action to the user
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    # Check if the sender is the id of Carlos
    start_message = (
        create_start_answer(**get_weekday_moment())
        if str(update.effective_user.id) == os.environ.get("ALLOWED_USER_ID")
        else "You are not allowed to use this bot."
    )

    # Send the start message to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message,
    )
