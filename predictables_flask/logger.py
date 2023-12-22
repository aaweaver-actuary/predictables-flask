import logging
from logging.handlers import RotatingFileHandler


# Create a logger
def create_logger(name: str) -> logging.Logger:
    """
    Create a logger for the application.

    Parameters
    ----------
    name : str
        The name of the logger.

    Returns
    -------
    logging.Logger
        A logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler
    handler = RotatingFileHandler(f"{name}.log", maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
