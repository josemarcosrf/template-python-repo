import logging.config
import os
import sys
from logging import Logger

import tqdm

from my_package import version
from my_package.constants import DEFAULT_LOG_DIR

LOG_DIR = os.getenv("LOG_DIR", DEFAULT_LOG_DIR)


__version__ = version.__version__


logger = logging.getLogger(__name__)


class TqdmStream(object):
    @classmethod
    def write(_, msg):
        tqdm.tqdm.write(msg, end="")

    @classmethod
    def flush(_):
        sys.stdout.flush()


def disable_lib_loggers():
    # disable other loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_default_config(
    level: str, fmt: str, filename: str = None, my_logger: Logger = None,
):
    _logger = my_logger or logger
    config_logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": fmt,},
            "colored": {
                "()": "coloredlogs.ColoredFormatter",
                "fmt": fmt,
                "field_styles": {
                    "asctime": {},
                    "hostname": {"color": "magenta"},
                    "levelname": {"color": "black", "bold": True},
                    "programname": {"color": "cyan"},
                    "name": {"color": "blue"},
                },
                "level_styles": {
                    # More style info at:
                    # https://coloredlogs.readthedocs.io/en/latest/api.html
                    "spam": {"color": "green", "faint": True},
                    "debug": {"color": "white", "faint": True},
                    "verbose": {"color": "blue"},
                    "info": {},
                    "notice": {"color": "cyan", "bold": True},
                    "warning": {"color": "yellow"},
                    "success": {"color": "green", "bold": True},
                    "error": {"color": "red"},
                    "critical": {"color": "red", "bold": True},
                },
            },
        },
        "handlers": {
            "console": {
                "level": level,
                "formatter": "colored",
                "class": "logging.StreamHandler",
                "stream": TqdmStream,  # so logging doesn't brake tqdm
                # "stream": sys.stdout,
            },
        },
        "loggers": {
            _logger.name: {"handlers": ["console"], "level": level,},
            "pika": {"handlers": ["console"], "level": "WARNING",},
            "asyncio": {"level": "WARNING",},
            "filelock": {"level": "WARNING",},
        },
    }

    if filename:
        config_logging["handlers"].update(
            {
                "rotate_file": {
                    "level": level,
                    "formatter": "standard",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": filename,
                    "when": "H",
                }
            }
        )
        config_logging["loggers"][_logger.name]["handlers"].append("rotate_file")

    return config_logging


def init_logger(
    level,
    my_logger: Logger = None,
    filename: str = None,
    fmt="%(asctime)s,%(msecs)03d %(levelname)-8s %(name)-45s:%(lineno)3d - %(message)-50s",
):
    """ Configures the given logger; format, logging level, style, etc """

    def add_notice_log_level():
        """ Creates a new 'notice' logging level """
        # inspired by:
        # https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
        NOTICE_LEVEL_NUM = 25
        logging.addLevelName(NOTICE_LEVEL_NUM, "NOTICE")

        def notice(self, message, *args, **kws):
            if self.isEnabledFor(NOTICE_LEVEL_NUM):
                self._log(NOTICE_LEVEL_NUM, message, args, **kws)

        logging.Logger.notice = notice

    # disable some library loggers
    disable_lib_loggers()

    # Add an extra logging level above INFO and below WARNING
    add_notice_log_level()

    if filename:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR, exist_ok=True)

        filename = os.path.join(LOG_DIR, filename)

    logging.config.dictConfig(
        get_default_config(level=level, filename=filename, fmt=fmt, my_logger=my_logger)
    )
