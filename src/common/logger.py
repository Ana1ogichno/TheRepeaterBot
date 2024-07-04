import logging
import sys

from src.config.settings import settings


class LoggerManager:
    # Base logger
    __base_log_name: str = settings.logger_settings.BASE_LOGGER_NAME
    __base_log_level: str = settings.logger_settings.BASE_LOGGER_LEVEL
    __base_log_format: str = settings.logger_settings.BASE_LOGGER_FORMAT

    # Postgres logger
    __psql_log_name: str = settings.logger_settings.POSTGRES_LOGGER_NAME
    __psql_log_level: str = settings.logger_settings.POSTGRES_LOGGER_LEVEL
    __psql_log_format: str = settings.logger_settings.POSTGRES_LOGGER_FORMAT

    @staticmethod
    def __configure_logger(logger: logging.Logger, level: str, format_str: str) -> None:
        logger.setLevel(level)
        logger.propagate = False

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(format_str))
        logger.addHandler(console_handler)

    @classmethod
    def __get_logger(cls, name: str, level: str, format_str: str) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            cls.__configure_logger(
                logger=logger,
                level=level,
                format_str=format_str,
            )
        return logger

    @classmethod
    def get_base_logger(cls) -> logging.Logger:
        return cls.__get_logger(
            name=cls.__base_log_name,
            level=cls.__base_log_level,
            format_str=cls.__base_log_format,
        )

    @classmethod
    def get_psql_logger(cls) -> logging.Logger:
        return cls.__get_logger(
            name=cls.__psql_log_name,
            level=cls.__psql_log_level,
            format_str=cls.__psql_log_format,
        )
