import logging


def init(filename=None, level=logging.DEBUG):
    log_fmt = '%(asctime)s - %(levelname)s - %(processName)s/%(threadName)s - %(message)s'
    logging.basicConfig(filename=filename, level=level, format=log_fmt)


def debug(*kwargs):
    logging.debug(*kwargs)


def info(*kwargs):
    logging.info(*kwargs)


def warn(*kwargs):
    logging.warn(*kwargs)


def error(*kwargs):
    logging.error(*kwargs)


def critical(*kwargs):
    logging.critical(*kwargs)


init(level=logging.INFO)
