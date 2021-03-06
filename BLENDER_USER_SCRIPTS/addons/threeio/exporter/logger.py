import os
import logging
import tempfile

from . import constants

LOG_FILE = None
LOGGER = None
FILE_NAME = 'threeio.export.log'

LEVELS = {
    constants.DEBUG: logging.DEBUG,
    constants.INFO: logging.INFO,
    constants.WARNING: logging.WARNING,
    constants.ERROR: logging.ERROR,
    constants.CRITICAL: logging.CRITICAL
}

def init(level=constants.DEBUG):
    global LOG_FILE
    LOG_FILE = os.path.join(tempfile.gettempdir(), FILE_NAME)
    with open(LOG_FILE, 'w'):
        pass

    global LOGGER
    LOGGER = logging.getLogger('ThreeIO.Export')
    LOGGER.setLevel(LEVELS[level])

    stream = logging.StreamHandler()
    stream.setLevel(LEVELS[level])

    format_ = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    formatter = logging.Formatter(format_)

    stream.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(LEVELS[level])
    file_handler.setFormatter(formatter)

    LOGGER.addHandler(stream)
    LOGGER.addHandler(file_handler)


def info(*args):
    LOGGER.info(*args)

def debug(*args):
    LOGGER.debug(*args)

def warning(*args):
    LOGGER.warning(*args)

def error(*args):
    LOGGER.error(*args)

def critical(*args):
    LOGGER.critical(*args)
