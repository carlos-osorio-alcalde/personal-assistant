import logging

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filemode="a",
    datefmt="%H:%M:%S",
    filename="assistantbot/logs/assistantbot.log",
)

# Set up the logger
logger = logging.getLogger(__name__)
