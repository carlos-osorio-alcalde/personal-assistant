from telegram.ext import MessageHandler

from assistantbot.ai.text.prompts.conversation import (
    CONVERSATION_BASE_TEMPLATE,
)
from assistantbot.conversation.text.callback import ConversationCallback


def message_handler() -> MessageHandler:
    """
    This function returns the message handler.

    Returns
    -------
    MessageHandler
        The message handler.
    """
    return MessageHandler(
        None,
        ConversationCallback(
            base_system_prompt=CONVERSATION_BASE_TEMPLATE
        ).create_response,
    )
