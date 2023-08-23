from typing import Optional

from langchain.chains import ConversationChain
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from assistantbot.ai.text.prompts.image_captioning import (
    IMAGE_CAPTION_PROMPT_REQUEST,
    IMAGE_CAPTION_PROMPT_WITHOUT_REQUEST,
)
from assistantbot.ai.vision.captioner import VisionCaptioner
from assistantbot.conversation.base import ConversationHandler
from assistantbot.conversation.chains import (
    get_conversation_chain,
    update_memory,
)
from assistantbot.utils.security import allowed_user_only


class VisionHandler(ConversationHandler):
    def __init__(self):
        """
        This object is used to handle the vision conversation.
        """
        super().__init__(filters.PHOTO)
        self.vision_captioner = VisionCaptioner()

    def handler(self) -> MessageHandler:
        """
        This function returns the message handler.

        Returns
        -------
        MessageHandler
            The message handler.
        """
        return MessageHandler(self._type, self.callback, block=False)

    async def _create_response(
        self,
        user_id: int,
        image_caption: str,
        image_message: Optional[str] = None,
        conversation_chain: Optional[ConversationChain] = None,
    ) -> str:
        """
        This method is used to create the response for the
        message handler.

        Parameters
        ----------
        image_caption : str
            The caption for the image.
        image_message : str, optional
            The message that comes with the image, by default None

        Returns
        -------
        str
            The response for the message handler.
        """
        # Create the entry for the caption in the context of the conversation
        entry_message = (
            IMAGE_CAPTION_PROMPT_REQUEST.format(
                caption=image_caption,
                image_message=f"Carlos' request: {image_message}",
            )
            if image_message is not None
            else IMAGE_CAPTION_PROMPT_WITHOUT_REQUEST.format(
                caption=image_caption
            )
        )

        # Add the caption to the context of the conversation
        response_message = await conversation_chain.apredict(
            input=entry_message
        )

        # Update the memory
        update_memory(user_id, conversation_chain)

        return response_message

    @allowed_user_only
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
        # Get the conversation chain
        conversation_chain = get_conversation_chain(update.effective_user.id)

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
        image_response = await self._create_response(
            user_id=update.effective_chat.id,
            image_caption=caption,
            image_message=image_message,
            conversation_chain=conversation_chain,
        )

        # Send the caption to the user
        await update.message.reply_text(image_response)
