import logging

from assistantbot.configuration import config

# Set up the paths
logging.captureWarnings(True)
logging.basicConfig(
    filename=config["ERROR_LOG_FILE"],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Set up the logger
logger = logging.getLogger(__name__)
