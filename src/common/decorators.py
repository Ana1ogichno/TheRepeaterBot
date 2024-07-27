from functools import wraps
from src.common.logger import LoggerManager

logger = LoggerManager.get_base_logger()


def logging_call(description: str = None):
    """Декоратор для логирования вызова функций"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            message: str = f"Start: {func.__name__}"

            if description:
                message = f"{message}, description: {description}"

            logger.info(message)

            return func(*args, **kwargs)

        return wrapper

    return decorator
