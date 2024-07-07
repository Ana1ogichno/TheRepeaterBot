from enum import Enum


class SchemasEnum(str, Enum):
    TELEGRAM = "telegram"
    USERS = "users"


class TelegramTablesEnum(str, Enum):
    CHANNEL = "channel"
    MEDIA = "media"
    POST = "post"


class DataUploadStatusEnum(str, Enum):
    NO_CHANNEL = "no_channel"
