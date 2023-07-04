import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Load environment variables
load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi, {message}",
    )


if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters=None, callback=message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
