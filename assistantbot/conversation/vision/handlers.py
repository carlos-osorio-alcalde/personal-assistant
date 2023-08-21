from typing import Optional

from langchain.chains import ConversationChain
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.ai.text.base_response import BaseResponse
from assistantbot.ai.text.prompts.image_captioning import (
    IMAGE_CAPTION_PROMPT,
    USER_PROMPT_TEMPLATE_CAPTIONING,
    AUTOMATIC_IMAGE_CAPTION,
)
from assistantbot.ai.vision.captioner import VisionCaptioner
from assistantbot.conversation.base import ConversationHandler


class VisionHandler(ConversationHandler):
    def __init__(
        self, conversacion_chain: Optional[ConversationChain] = None
    ):
        """
        This object is used to handle the vision conversation.

        Parameters
        ----------
        conversacion_chain : Optional[ConversationChain], optional
            The conversation chain to add the messages to the
            context of the conversation, by default None
        """
        super().__init__(filters.PHOTO)
        self.conversation_chain = conversacion_chain
        self.vision_captioner = VisionCaptioner()

    def handler(self) -> MessageHandler:
        """
        This function returns the message handler.

        Returns
        -------
        MessageHandler
            The message handler.
        """
        return MessageHandler(self._type, self.callback)

    async def callback(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        This function is called when a text message is sent to the bot.

        Parameters
        ----------
        update : Update
            The update object from Telegram.
        context : CallbackContext
            The context object from Telegram.
        """
        # Send the chat action
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="upload_photo"
        )

        # Get the image from the message
        image = await update.message.photo[-1].get_file()

        # Get the caption for the image
        caption = self.vision_captioner.get_caption(image.file_path)

        # Get the message using the caption
        image_response = BaseResponse(
            IMAGE_CAPTION_PROMPT, USER_PROMPT_TEMPLATE_CAPTIONING
        ).create_response

        # Get the message to send to the user
        response = image_response(caption=caption)

        # Send the caption to the user
        await update.message.reply_text(
            response + AUTOMATIC_IMAGE_CAPTION.format(caption=caption)
        )
