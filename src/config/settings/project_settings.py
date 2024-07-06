from typing import Any

from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    # --================ Project Settings ================-- #

    # Main

    API_ID: int = Field("default_api_id", alias="API_ID")
    API_HASH: str = Field("default_api_hash", alias="API_HASH")
    BOT_TOKEN: str | None = None

    @field_validator("BOT_TOKEN", mode="before")
    def create_bot_token(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return f"{values.data.get('API_ID')}:" f"{values.data.get('API_HASH')}"

    # Media

    # PATH_TO_MEDIA_DIRECTORY: str = "C:\Projects\TheRepeaterBot\TheRepeaterBot-Consumer\src\modules\data_upload\media"
