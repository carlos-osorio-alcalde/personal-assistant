import time
from assistantbot import bot, clean_all_conversations
from contextlib import contextmanager


@contextmanager
def handle_expections():
    try:
        yield
    except (RuntimeWarning, Exception, RuntimeError) as e:
        bot.logger.exception(e)
        clean_all_conversations()
        time.sleep(5)


if __name__ == "__main__":
    while True:
        with handle_expections():
            bot.main()


