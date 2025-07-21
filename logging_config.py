import sys
from loguru import logger
import os


def setup_logging():
    """Logging configuration.
    This function should be called at the start of the application.
    """

    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    logger.remove()  # Remove the default logger
    logger.add(sys.stdout, level="INFO")
    logger.add(
        os.path.join(logs_dir, "app.log"),
        level="DEBUG",
        rotation="3MB",
        retention="30 days",
        compression="zip",
    )
    logger.add(
        os.path.join(logs_dir, "error.log"),
        level="ERROR",
        rotation="5MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    logger.info("Logging is set up successfully.")
