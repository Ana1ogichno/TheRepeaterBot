from pypika import Query, Schema, Table
from uuid import uuid4

from src.common.logger import LoggerManager
from .utils import check_exist_channel
from ...config.db import DBSessionsManager

logger = LoggerManager.get_psql_logger()


class UploadData:
    @staticmethod
    async def upload_data_to_psql(data):
        logger.info("Check existing channel in DB")

        source_channel_sid = await check_exist_channel(data.peer_id.channel_id)

        if not source_channel_sid:
            logger.info("Channel with this sid not found")
            return None

        logger.info("Extracting data for upload to DB")

        sid = uuid4()

        raw_text = None
        if data.message:
            raw_text = data.message

        created_at = data.date

        value = (sid, source_channel_sid, raw_text, created_at)

        telegram = Schema("telegram")
        post = Table("post")

        logger.info("Upload data to DB")

        query = (
            Query.into(telegram.post)
            .columns(post.sid, post.source_channel_sid, post.raw_text, post.created_at)
            .insert(value)
            .get_sql()
        )

        db_client = DBSessionsManager.pg_client

        with db_client.cursor() as cursor:
            try:
                cursor.execute(query)
            except Exception as e:
                logger.error(f"{e}")
                db_client.rollback()

            db_client.commit()
