from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    # --================ S3 Settings ================-- #

    # Main Settings
    S3_HOST: str = Field("def_host", alias="S3_HOST")
    S3_PORT: int = Field(9000, alias="S3_PORT")
    S3_ACCESS_KEY: str = Field("default_access_key", alias="S3_ACCESS_KEY")
    S3_SECRET_KEY: str = Field("default_secret_key", alias="S3_SECRET_KEY")
    S3_REGION_NAME: str = Field("default_region_name", alias="S3_REGION_NAME")
    S3_URL: str | None = None

    # Bucket Settings
    MEDIA_BUCKET_NAME: str = Field("default_media_bucket_name", env="MEDIA_BUCKET_NAME")
    GRAPH_BUCKET_NAME: str = Field("graphs", env="GRAPH_BUCKET_NAME")

    @field_validator("S3_URL", mode="before")
    def s3_url(cls, v: str | None, values: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        return f"http://{values.data.get('S3_HOST')}:" f"{values.data.get('S3_PORT')}"
