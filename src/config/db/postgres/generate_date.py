from src.common.consts.enums import SchemasEnum, TelegramTablesEnum
from src.modules.data_upload.data_upload import DataUploadUtils
from src.common.consts.consts import ConstList
from src.common.logger import LoggerManager
from src.config.bot.session import client
from pypika import Query, Schema, Table
from uuid import uuid4
import datetime

_logger = LoggerManager.get_psql_logger()
_data_upload_utils = DataUploadUtils()


async def generate_channels(channels: list[str]):
    await client.start()
    await client.connect()
    telegram_schema = Schema(SchemasEnum.TELEGRAM.value)
    channel_table = Table(TelegramTablesEnum.CHANNEL.value)
    all_columns = "*"

    counter = 0
    for channel_link in channels:
        channel = await client.get_entity(channel_link)
        if not channel:
            _logger.warning(f"Channel with link={channel_link} not found")
            continue
        source_channel = await _data_upload_utils.execute_query_with_result(
            query=(
                Query()
                .from_(telegram_schema.channel)
                .select(all_columns)
                .where(channel_table.id == channel.id)
                .get_sql()
            )
        )
        if source_channel:
            _logger.info(f"Channel with link={channel_link} already exists")
            continue

        value = (
            uuid4(),
            channel.id,
            channel.title,
            channel_link,
            datetime.datetime.now(datetime.UTC),
            True,
        )
        await _data_upload_utils.execute_query(
            query=(
                Query.into(telegram_schema.channel)
                .columns(
                    channel_table.sid,
                    channel_table.id,
                    channel_table.name,
                    channel_table.link,
                    channel_table.created_at,
                    channel_table.is_source,
                )
                .insert(value)
                .get_sql()
            )
        )
        counter += 1
    _logger.info(f"Successfully generated {counter} channels")


async def generate_data():
    _logger.info("Start initialization data")

    _logger.info("Start generating channels")
    await generate_channels(ConstList.CHANNEL_LIST)
    _logger.info("End generating channels")

    _logger.info("End initialization data")
