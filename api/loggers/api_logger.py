import logging
from logging.handlers import TimedRotatingFileHandler

from uvicorn.logging import ColourizedFormatter

from api.config import API_LOG_FILE_LOCATION, settings

_logger = logging.getLogger("api_logger")
_logger.setLevel(settings.run.logging)

# Console Handler
console_handler = logging.StreamHandler()
console_formatter = ColourizedFormatter(
    "%(levelprefix)s API-LOGGER -> %(message)s", use_colors=True
)
console_handler.setFormatter(console_formatter)

# File Handler
file_handler = TimedRotatingFileHandler(API_LOG_FILE_LOCATION)
file_formatter = logging.Formatter(
    "time: %(asctime)s, %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)


_logger.addHandler(console_handler)
_logger.addHandler(file_handler)
