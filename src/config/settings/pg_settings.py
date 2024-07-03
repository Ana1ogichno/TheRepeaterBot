from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # --================ Postgres Settings ================-- #

    # Main

    POSTGRES_HOST: str = Field("0.0.0.0", alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, alias="POSTGRES_PORT")
    POSTGRES_USER: str = Field("test", alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("password", alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("default_db", alias="POSTGRES_DB")
