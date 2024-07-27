from telethon import events

from src.common.consts import DataUploadStatusEnum
from src.common.consts.consts import ConstList
from src.common.logger import LoggerManager
from src.config.bot.session import client
from src.modules.data_upload import UploadData


logger = LoggerManager.get_base_logger()


@client.on(events.NewMessage(chats=ConstList.CHANNEL_LIST))
async def channels_handler(event):
    upload_data_module = UploadData()
    logger.info(
        "# -======================== START PROCESSING MESSAGE ========================- # \n"
    )
    logger.info(
        f"Receiving message from channel with "
        f"{event.message.peer_id.channel_id} id"
    )

    logger.info("Uploading data to DB")
    post_sid = await upload_data_module.upload_data_to_psql(event.message)

    if post_sid is DataUploadStatusEnum.NO_CHANNEL:
        logger.info(
            "# -======================== END PROCESSING MESSAGE ========================- # \n"
        )
        return None

    logger.info("Uploading media to S3 storage")

    await upload_data_module.upload_media(event.message, post_sid=post_sid)

    logger.info(
        "# -======================== END PROCESSING MESSAGE ========================- # \n"
    )


logger.info("Start TheRepeaterBot")
client.start()
client.run_until_disconnected()
