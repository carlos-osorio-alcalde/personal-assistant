from typing import Optional

from langchain.chains import ConversationChain
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.ai.text.prompts.image_captioning import (
    IMAGE_CAPTION_PROMPT,
)
from assistantbot.ai.vision.captioner import VisionCaptioner
from assistantbot.conversation import TextHandler
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

    def _create_response(
        self, image_caption: str, image_message: str
    ) -> str:
        """
        This method is used to create the response for the
        message handler.

        Parameters
        ----------
        image_caption : str
            The caption for the image.
        image_message : str
            The message that comes with the image.

        Returns
        -------
        str
            The response for the message handler.
        """
        # If the conversation chain is not specified, use the default one
        # However, this should not happen
        if self.conversation_chain is None:
            self.conversation_chain = TextHandler().conversation_chain

        # Create the entry for the caption in the context of the conversation
        entry_message = IMAGE_CAPTION_PROMPT.format(
            caption=image_caption,
            image_message=f"Carlos's request: {image_message}",
        )

        # Add the caption to the context of the conversation
        response_message = self.conversation_chain.predict(
            input=entry_message
        )

        return response_message

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

        # Get the message that comes with the image
        image_message = update.message.caption

        # Get the caption for the image
        caption = self.vision_captioner.get_caption(image.file_path)

        # Get the message using the caption
        image_response = self._create_response(
            image_caption=caption, image_message=image_message
        )

        # Send the caption to the user
        await update.message.reply_text(image_response)
