import logging
import sys


def init_logger(
    logger_name: str, *, date_fmt: str = "%Y-%m-%d %H:%M:%S"
) -> None:
    """Initialize the logger with appropriate logger name,
    set the threshold to logging level of the logger to `INFO`,
    create a stream-based handler that writes the log entries into
    the standard output stream, create a formatter for the logs,
    set the created formatter as the formatter of the handler,
    and add the created handler to the logger.

    :param logger_name: A logger name to use.
    :param date_fmt: Format of the date.
    :return: None.
    """
    logger = logging.getLogger(name=logger_name)

    logger.setLevel(level=logging.INFO)

    handler = logging.StreamHandler(stream=sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=date_fmt,
    )

    handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=handler)
