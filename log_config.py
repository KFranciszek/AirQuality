
import logging
import logging.handlers

def setup_logger(name):
    """
    Set up a logger with specified name, which sends logs to Papertrail service.

    This logger is set at the INFO logging level and logs are formatted as:
    'name of logger' - 'logging level' - 'log message'.

    Parameters
    ----------
    name : str
        The name of the logger.

    Returns
    -------
    logger : logging.Logger
        An instance of a logger which sends logs to the Papertrail service.

    Examples
    --------
    >>> logger = setup_logger("my_app")
    >>> logger.info("This is an info log.")

    """
    # Creating a logger
    logger = logging.getLogger(name)

    # Set the login level
    logger.setLevel(logging.INFO)

    # Creating a handler which sends logs to Papertrail
    handler = logging.handlers.SysLogHandler(address = ('logs3.papertrailapp.com', 34215))

    # Setting the log format
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Adding the handler to the logger
    logger.addHandler(handler)

    return logger