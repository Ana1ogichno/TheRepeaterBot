from uuid import uuid4

from src.common.logger import LoggerManager
from .utils import check_exist_channel

logger = LoggerManager.get_psql_logger()


class UploadData:
    @staticmethod
    async def upload_data_to_psql(data):
        logger.info("Check existing channel in DB")

        source_channel_sid = await check_exist_channel(data.original_update.message.peer_id.channel_id)

        if not source_channel_sid:
            logger.info("Channel with this sid not found")
            return None

        logger.info("Extracting data for upload to DB")

        sid = uuid4()

        if data.original_update.message.message:
            raw_text = data.original_update.message.message

        is_publication = False






