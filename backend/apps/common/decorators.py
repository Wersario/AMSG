from functools import wraps
import logging

logger = logging.getLogger(__name__)


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Executing {func.__name__}')
        return func(*args, **kwargs)

    return wrapper