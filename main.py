from telethon import events

from src.modules.data_upload import UploadData
from src.common.consts.consts import ConstList
from src.common.logger import LoggerManager
from src.config.bot.session import client
from src.config.settings import settings


bot_token = settings.project_settings.BOT_TOKEN


logger = LoggerManager.get_base_logger()


@client.on(events.NewMessage(chats=ConstList.channel_list))
async def channels_handler(event):
    logger.info(f"Receiving message from channel with "
                f"{event.original_update.message.peer_id.channel_id} sid")

    logger.info("Uploading data to DB")
    await UploadData.upload_data_to_psql(event)

    await event.original_update.message.download_media()


logger.info("Start TheRepeaterBot")
client.start()
client.run_until_disconnected()
