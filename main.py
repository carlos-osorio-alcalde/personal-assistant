import time
from assistantbot import bot
from contextlib import contextmanager


@contextmanager
def handle_expections():
    try:
        yield
    except (RuntimeWarning, Exception, RuntimeError) as e:
        bot.logger.exception(e)
        time.sleep(5)


if __name__ == "__main__":
    while True:
        with handle_expections():
            bot.main()
