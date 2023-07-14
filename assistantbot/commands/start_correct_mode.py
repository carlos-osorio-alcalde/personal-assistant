from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from assistantbot.ai.text.base_response import BaseResponse
from assistantbot.ai.text.prompts.correct_mode import (
    CORRECT_MODE_PROMPT_TEMPLATE,
    USER_PROMPT_TEMPLATE,
)
from assistantbot.commands.base import BaseCommand
from assistantbot.commands.end_correct_mode import EndCorrectModeCommand

# This variable will store the message to correct
state_message = ""


class StartCorrectModeCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command = "start_correct_mode"
        self._fallback_command = "end_correct_mode"

    @staticmethod
    async def command_callback(
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
        Hey Carlos! Send me a message to correct your grammar. I pledge to 
        not make a lot of changes.
        """

        # First, the bot sends the option to write the message to correct
        await update.message.reply_text(
            entry_message, reply_markup=ReplyKeyboardRemove()
        )

        return state_message

    @staticmethod
    async def _command_callback(
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
        # Send the typing action to the user
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # Get the message to correct
        message = update.effective_message.text

        # Instantiate the AI response
        get_corrected_message = BaseResponse(
            CORRECT_MODE_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE
        ).create_response
        corrected_message = get_corrected_message(message=message)

        # The bot sends the message to correct
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=corrected_message,
        )

    def command_handler(self) -> CommandHandler:
        """
        This function returns the handler for the correct command.

        Returns
        -------
        CommandHandler
            The command handler.
        """
        return ConversationHandler(
            entry_points=[
                CommandHandler(self._command, self.command_callback)
            ],
            states={
                state_message: [
                    MessageHandler(
                        filters.TEXT & (~filters.COMMAND),
                        self._command_callback,
                    )
                ]
            },
            fallbacks=[
                CommandHandler(
                    self._fallback_command,
                    EndCorrectModeCommand().command_callback,
                )
            ],
        )
