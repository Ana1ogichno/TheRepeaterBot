import os
import shutil

from pypika import Query, Schema, Table, Column
from uuid import uuid4, UUID

from src.common.logger import LoggerManager
from src.config.settings import settings
from .utils import check_exist_channel
from ...config.db import DBSessionsManager

logger = LoggerManager.get_base_logger()
psql_logger = LoggerManager.get_psql_logger()
s3_logger = LoggerManager.get_s3_logger()


class UploadData:
    @staticmethod
    async def upload_data_to_psql(data):
        psql_logger.info("Check existing channel in DB")

        source_channel_sid = await check_exist_channel(data.peer_id.channel_id)

        if not source_channel_sid:
            psql_logger.info("Channel with this sid not found")
            return None

        db_client = DBSessionsManager.pg_client

        if not data.message and data.grouped_id:
            telegram_schema = Schema("telegram")
            post_table = Table("post")
            sid = Column("sid")

            get_post_query = (
                Query()
                .from_(telegram_schema.post)
                .select(sid)
                .where(post_table.grouped_id == data.grouped_id)
                .get_sql()
            )

            with db_client.cursor() as cursor:
                try:
                    cursor.execute(get_post_query)
                    post = cursor.fetchall()
                    if post[0][0]:
                        psql_logger.info(
                            f"This message with media for group_id {data.grouped_id}"
                        )
                        return post[0][0]

                except Exception as e:
                    psql_logger.error(f"{e}")
                    db_client.rollback()

                db_client.commit()

        if not data.message:
            data.message = None

        sid = uuid4()

        psql_logger.info("Extracting data for upload to DB")

        value = (sid, source_channel_sid, data.message, data.grouped_id, data.date)

        telegram_schema = Schema("telegram")
        post_table = Table("post")

        psql_logger.info("Upload data to DB")

        query = (
            Query.into(telegram_schema.post)
            .columns(
                post_table.sid,
                post_table.source_channel_sid,
                post_table.raw_text,
                post_table.grouped_id,
                post_table.created_at,
            )
            .insert(value)
            .get_sql()
        )

        with db_client.cursor() as cursor:
            try:
                cursor.execute(query)
            except Exception as e:
                psql_logger.error(f"{e}")
                db_client.rollback()

            db_client.commit()

        return sid

    @staticmethod
    async def upload_media(data, post_sid: UUID):
        # s3_client = DBSessionsManager.s3_client

        # print(data.media.photo.sizes[0].bytes)
        #
        # s3_client.upload_fileobj(data.media.photo.sizes[0].bytes, "media", "asdf.jpg")

        db_client = DBSessionsManager.pg_client

        if data.media is None:
            logger.info("No media provided")
            return None

        logger.info("Downloading media")

        dir_name = f"media_{uuid4()}"

        directory = f"src/modules/data_upload/media/{dir_name}"
        os.mkdir(directory)

        await data.download_media(file=directory)

        media = os.listdir(directory)

        filename = str(uuid4()) + f".{media[0].split(".")[-1]}"

        path = f"{post_sid}/{filename}"

        s3_logger.info("Upload file")

        s3_client = DBSessionsManager.s3_client

        s3_client.upload_file(
            f"{directory}/{media[0]}", settings.s3.MEDIA_BUCKET_NAME, path
        )

        logger.info("Create record in media table")

        telegram_schema = Schema("telegram")
        media_table = Table("media")

        value = (uuid4(), post_sid, path, data.date)

        query = (
            Query.into(telegram_schema.media)
            .columns(
                media_table.sid,
                media_table.post_sid,
                media_table.path,
                media_table.created_at,
            )
            .insert(value)
            .get_sql()
        )

        with db_client.cursor() as cursor:
            try:
                cursor.execute(query)
            except Exception as e:
                psql_logger.error(f"{e}")
                db_client.rollback()

            db_client.commit()

        shutil.rmtree(directory)
