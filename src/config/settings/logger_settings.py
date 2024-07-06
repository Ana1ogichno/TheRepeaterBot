class LoggerSettings:
    # --================ Base Logger Settings ================-- #

    BASE_LOGGER_NAME: str = "BASE"
    BASE_LOGGER_LEVEL: str = "INFO"
    BASE_LOGGER_FORMAT: str = (
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    # --================ Postgres Logger Settings ================-- #

    POSTGRES_LOGGER_NAME: str = "POSTGRES"
    POSTGRES_LOGGER_LEVEL: str = "INFO"
    POSTGRES_LOGGER_FORMAT: str = (
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    # --================ S3 Logger Settings ================-- #

    S3_LOGGER_NAME: str = "S3"
    S3_LOGGER_LEVEL: str = "INFO"
    S3_LOGGER_FORMAT: str = (
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
