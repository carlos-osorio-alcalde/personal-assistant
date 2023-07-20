import time
from assistantbot import bot


if __name__ == "__main__":
    while True:
        try:
            # Start the bot
            bot.main()
        except Exception as e:
            # Log the exception
            bot.logger.exception(e)

            # Sleep for 5 seconds
            time.sleep(5)

            # Restart the bot
            continue
