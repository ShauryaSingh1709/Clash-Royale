














import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from backend.config.settings import Config


class ColoredFormatter(logging.Formatter):





    COLORS = {
        "DEBUG":    "\033[36m",
        "INFO":     "\033[32m",
        "WARNING":  "\033[33m",
        "ERROR":    "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:

        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname:8}{self.RESET}"
        return super().format(record)


def get_logger(name: str) -> logging.Logger:









    logger = logging.getLogger(name)


    if logger.handlers:
        return logger

    logger.setLevel(Config.LOG_LEVEL)




    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(Config.LOG_LEVEL)
    console_formatter = ColoredFormatter(
        fmt=Config.LOG_FORMAT,
        datefmt=Config.LOG_DATE_FORMAT
    )
    console_handler.setFormatter(console_formatter)




    log_file: Path = Config.LOGS_PATH / "app.log"
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(
        fmt=Config.LOG_FORMAT,
        datefmt=Config.LOG_DATE_FORMAT
    )
    file_handler.setFormatter(file_formatter)


    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


    logger.propagate = False

    return logger