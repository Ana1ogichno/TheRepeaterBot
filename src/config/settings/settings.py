from .logger_settings import LoggerSettings
from .pg_settings import PostgresSettings
from .project_settings import ProjectSettings
from .s3_settings import S3Settings


class Settings:
    logger_settings = LoggerSettings()
    pg_settings: PostgresSettings = PostgresSettings()
    project_settings: ProjectSettings = ProjectSettings()
    s3: S3Settings = S3Settings()


settings: Settings = Settings()
