from .logger_settings import LoggerSettings
from .pg_settings import PostgresSettings
from .project_settings import ProjectSettings


class Settings:
    logger_settings = LoggerSettings()
    pg_settings: PostgresSettings = PostgresSettings()
    project_settings: ProjectSettings


settings: Settings = Settings()
