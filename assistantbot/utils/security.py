import functools
import os
from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes


def allowed_user_only(func: Callable) -> Callable[[Update], None]:
    """
    Decorator to restrict a function's execution to the allowed user.

    Parameters
    ----------
    func : callable
        The function to be decorated.

    Returns
    -------
    callable
        The decorated function.
    """

    @functools.wraps(func)
    async def wrapper(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args,
        **kwargs
    ):
        if str(update.effective_user.id) == os.environ.get(
            "ALLOWED_USER_ID"
        ):
            return await func(self, update, context, *args, **kwargs)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="User not allowed to use this feature of the bot ❌",
            )

    return wrapper
