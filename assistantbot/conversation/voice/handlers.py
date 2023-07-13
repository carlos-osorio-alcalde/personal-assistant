from telegram.ext import MessageHandler, filters, CallbackContext
from telegram import Update
from assistantbot.conversation.base import ConversationHandler


class VoiceHandler(ConversationHandler):
    def __init__(self):
        super().__init__(filters.VOICE)

    def handler(self) -> MessageHandler:
        return MessageHandler(self._type, self.callback)

    async def callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        This function is called when a voice message is sent to the bot.

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : _type_
            The context object from Telegram.
        """
        # If a voice message is sent, the bot will reply with a text message
        # containing the text of the voice message.
        voice_file = update.message.voice

        # Get the voice message
        voice_file = await context.bot.get_file(voice_file.file_id)
        await voice_file.download_to_drive("voice.ogg")
