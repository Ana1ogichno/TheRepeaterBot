import os
import shutil

from pypika import Query, Schema, Table
from uuid import uuid4, UUID
from src.common import logging_call
from src.common.logger import LoggerManager
from .utils import DataUploadUtils
from ...common.consts import SchemasEnum, TelegramTablesEnum, DataUploadStatusEnum
from ...config.settings import settings


class UploadData:
    def __init__(self):
        self._data_upload_utils = DataUploadUtils()
        self._logger = LoggerManager.get_base_logger()
        self._psql_logger = LoggerManager.get_psql_logger()
        self._s3_logger = LoggerManager.get_s3_logger()

    @logging_call()
    async def upload_data_to_psql(self, message):
        # Variable for sqlquery builder
        telegram_schema = Schema(SchemasEnum.TELEGRAM.value)
        channel_table = Table(TelegramTablesEnum.CHANNEL.value)
        post_table = Table(TelegramTablesEnum.POST.value)
        all_columns = "*"

        self._logger.info("Check existing channel in DB")

        source_channel = await self._data_upload_utils.execute_query_with_result(
            query=(
                Query()
                .from_(telegram_schema.channel)
                .select(all_columns)
                .where(channel_table.id == message.peer_id.channel_id)
                .get_sql()
            )
        )

        if not source_channel:
            self._psql_logger.info(
                f"Channel with id = {message.peer_id.channel_id} not found"
            )
            return DataUploadStatusEnum.NO_CHANNEL

        if not message.message and message.grouped_id:
            self._logger.info(
                f"Check existing post with grouped_id = {message.grouped_id}"
            )

            post = await self._data_upload_utils.execute_query_with_result(
                query=(
                    Query()
                    .from_(telegram_schema.post)
                    .select(all_columns)
                    .where(post_table.grouped_id == message.grouped_id)
                    .get_sql()
                )
            )

            if post:
                self._psql_logger.info(
                    f"This message with media for group_id = {message.grouped_id}"
                )
                return post[0][0]

        if not message.message:
            message.message = None

        self._logger.info("Extracting data for upload to DB")

        sid = uuid4()
        value = (
            sid,
            source_channel[0][0],
            message.message,
            message.grouped_id,
            message.date,
        )

        self._psql_logger.info("Upload data to DB")

        await self._data_upload_utils.execute_query(
            query=(
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
        )

        return sid

    @logging_call()
    async def upload_media(self, message, post_sid: UUID):
        # Variable for sqlquery builder
        telegram_schema = Schema("telegram")
        media_table = Table("media")

        if message.media is None:
            self._logger.info("Message contains no media")
            return None

        self._logger.info("Creating directory for download media")
        dir_name = f"{uuid4()}"
        directory = f"src/modules/data_upload/tmp_media/{dir_name}"
        os.mkdir(directory)

        self._logger.info(f"Downloading media in '{dir_name}' directory")

        await message.download_media(file=directory)

        self._logger.info("Preparing for upload media to S3 storage")
        media = os.listdir(directory)
        filename = str(uuid4()) + f".{media[0].split(".")[-1]}"
        path = f"{post_sid}/{filename}"

        self._s3_logger.info("Upload media to S3 storage")

        await self._data_upload_utils.upload_to_s3(
            path_to_file=f"{directory}/{media[0]}",
            bucket=settings.s3.MEDIA_BUCKET_NAME,
            path_in_s3=path,
        )

        self._psql_logger.info("Create record in 'media' table")

        value = (uuid4(), post_sid, path, message.date)

        await self._data_upload_utils.execute_query(
            query=(
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
        )

        self._logger.info("Removing media")

        shutil.rmtree(directory)
