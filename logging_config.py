from loguru import logger
import sys


def setup_logging():
    logger.remove()  # Remove the default logger
    logger.add(sys.stdout, level="INFO")
    logger.add(
        "app.log", level="DEBUG", rotation="3MB", retention="30 days", compression="zip"
    )
    logger.add(
        "error.log",
        level="ERROR",
        rotation="5MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    logger.info("Logging is set up successfully.")
