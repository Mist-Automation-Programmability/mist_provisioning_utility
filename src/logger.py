import logging  # https://docs.python.org/3/library/logging.html?highlight=logging#module-logging
from sys import stdout
file_log_fmt = '%(asctime)s [%(levelname)-7s][%(name)s]: %(message)s'
console_log_fmt = '[%(module)-6s - %(funcName)-12s: %(lineno)-3d][%(levelname)-7s] %(message)s'
date_fmt = "%Y-%m-%d %H:%M:%S %Z"


def create_logger(level: str = "DEBUG") -> logging.Logger:
    """
    Configure script logging object

    :param str level: Logging level (ERROR, WARNING, INFO, DEBUG)

    :return logging.Logger: Custom logging object
    """

    # Configure basic logging options
    logging.basicConfig(level=logging.INFO, format=file_log_fmt, datefmt=date_fmt)
    other_logger = logging.getLogger()
    other_logger.handlers.clear()

    # Create custom logging object
    log = logging.getLogger("mist_provisioning_utility")
    log.handlers.clear()

    # Configure custom logging object
    log.setLevel(level=level)
    log.propagate = False

    # Create site_creator.log file handler
    file_formatter = logging.Formatter(file_log_fmt)
    file_formatter.datefmt = date_fmt
    fh = logging.FileHandler("mist_provisioning_utility.log")
    fh.formatter = file_formatter
    fh.setLevel(level=level)
    log.addHandler(fh)

    # Create site_creator stream handler
    console_formatter = logging.Formatter(console_log_fmt)
    sh = logging.StreamHandler(stream=stdout)
    sh.formatter = console_formatter
    sh.setLevel(level=level)
    log.addHandler(sh)

    # Return custom logging object
    return log


logger = create_logger()
