"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Logging System
==========================================================================

Professional logging utility with colored console output and file logging.

Usage:
    from backend.utils.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Application started")
    logger.error("Something went wrong")
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from backend.config.settings import Config


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log levels in console output.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG":    "\033[36m",   # Cyan
        "INFO":     "\033[32m",   # Green
        "WARNING":  "\033[33m",   # Yellow
        "ERROR":    "\033[31m",   # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Apply color to the log level name."""
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname:8}{self.RESET}"
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger instance.

    Args:
        name (str): Logger name (typically __name__ of the module)

    Returns:
        logging.Logger: Configured logger with console + file handlers
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(Config.LOG_LEVEL)

    # ────────────────────────────────────────────────────────
    # Console Handler (with colors)
    # ────────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(Config.LOG_LEVEL)
    console_formatter = ColoredFormatter(
        fmt=Config.LOG_FORMAT,
        datefmt=Config.LOG_DATE_FORMAT
    )
    console_handler.setFormatter(console_formatter)

    # ────────────────────────────────────────────────────────
    # File Handler (rotating logs)
    # ────────────────────────────────────────────────────────
    log_file: Path = Config.LOGS_PATH / "app.log"
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(
        fmt=Config.LOG_FORMAT,
        datefmt=Config.LOG_DATE_FORMAT
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent duplicate logs from root logger
    logger.propagate = False

    return logger