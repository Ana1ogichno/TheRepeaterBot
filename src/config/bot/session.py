from telethon import TelegramClient

from src.config.settings import settings

client = TelegramClient(
    "anon", settings.project_settings.API_ID, settings.project_settings.API_HASH
)
