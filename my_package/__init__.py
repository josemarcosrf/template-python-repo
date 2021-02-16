import logging.config
import os

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


def disable_lib_loggers():
    # disable other loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_default_config(level: str, filename: str, fmt: str):
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
            "rotate_file": {
                "level": level,
                "formatter": "standard",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": filename,
                "when": "H",
            },
        },
        "loggers": {
            logger.name: {"handlers": ["console", "rotate_file"], "level": level,},
            "pika": {"handlers": ["console"], "level": "WARNING",},
            "asyncio": {"level": "WARNING",},
            "filelock": {"level": "WARNING",},
        },
    }

    return config_logging


# TODO: Make filename optional!
def init_logger(
    level,
    filename: str,
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

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logging.config.dictConfig(
        get_default_config(
            level=level, filename=os.path.join(LOG_DIR, filename), fmt=fmt
        )
    )
