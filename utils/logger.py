"""
Centralized logging configuration.

Writes structured logs to both the console (coloured) and a daily
rotating file under the ``logs/`` directory.
"""

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

_LOGS_DIR = "logs"
os.makedirs(_LOGS_DIR, exist_ok=True)

_LOG_FILE = os.path.join(_LOGS_DIR, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _build_console_handler() -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    return handler


def _build_file_handler() -> TimedRotatingFileHandler:
    handler = TimedRotatingFileHandler(
        _LOG_FILE, when="midnight", interval=1, backupCount=14, encoding="utf-8"
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    return handler


def get_logger(name: str) -> logging.Logger:
    """Return a logger with console and file handlers attached."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(_build_console_handler())
        logger.addHandler(_build_file_handler())
        logger.propagate = False

    return logger
