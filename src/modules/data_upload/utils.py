from pypika import Query, Schema, Table

from src.common.logger import LoggerManager
from src.config.db.session import DBSessionsManager


logger = LoggerManager.get_psql_logger()


async def check_exist_channel(channel_id: int):
    telegram = Schema("telegram")
    channel = Table("channel")

    query = (
        Query()
        .from_(telegram.channel)
        .select("*")
        .where(channel.id == channel_id)
        .get_sql()
    )
    db_client = DBSessionsManager.pg_client

    with db_client.cursor() as cursor:
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                return data[0][0]

        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    return False
