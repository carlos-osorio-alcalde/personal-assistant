import time
from assistantbot import bot
import warnings
from contextlib import contextmanager


# Set the warnings to raise exceptions
warnings.filterwarnings("error")


@contextmanager
def log_exception():
    try:
        yield
    except (RuntimeWarning, Exception) as e:
        bot.logger.exception(e)
        time.sleep(5)


if __name__ == "__main__":
    while True:
        with log_exception():
            bot.main()
