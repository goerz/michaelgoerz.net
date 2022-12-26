"""Project-Logger."""

import logging
from colorama import Fore, Style


FMT = "%(levelname)s - %(message)s"


FORMATS = {
    logging.DEBUG: Fore.GREEN + FMT + Style.RESET_ALL,
    logging.INFO: "%(message)s",
    logging.WARNING: Fore.RED + FMT + Style.RESET_ALL,
    logging.ERROR: Style.BRIGHT + Fore.RED + FMT + Style.RESET_ALL,
    logging.CRITICAL: Style.BRIGHT + Fore.RED + FMT + Style.RESET_ALL,
}


FORMATTERS = {
    level: logging.Formatter(FORMATS[level])
    for level in [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]
}


class MultiFormatter(logging.Formatter):
    """Delegate to different formatter for each level."""

    def format(self, record):
        formatter = FORMATTERS.get(record.levelno)
        return formatter.format(record)


LOG = logging.getLogger("StaticSiteGenerator")
LOG.propagate = False
LOG.setLevel(logging.INFO)

_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)
_ch.setFormatter(MultiFormatter())

LOG.addHandler(_ch)
