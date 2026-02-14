import logging
import sys
from datetime import datetime

# ANSI color codes
COLORS = {
    "DEBUG": "\033[94m",    # blue
    "INFO": "\033[92m",     # green
    "WARNING": "\033[93m",  # yellow
    "ERROR": "\033[91m",    # red
    "CRITICAL": "\033[95m", # magenta
}
RESET = "\033[0m"


class FancyFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, "")
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        message = (
            f"{log_color}"
            f"[{timestamp}] "
            f"{record.levelname:<8} "
            f"{record.filename}:{record.lineno} "
            f"{record.funcName}() → "
            f"{record.getMessage()}"
            f"{RESET}"
        )
        return message


def get_logger(name: str = "app", level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger  # prevent duplicate handlers

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(FancyFormatter())

    logger.addHandler(handler)
    return logger
