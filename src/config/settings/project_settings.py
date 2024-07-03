from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # --================ Project Settings ================-- #

    # Main
