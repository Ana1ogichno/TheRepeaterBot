from src.common.logger import LoggerManager
from src.config.db import DBSessionsManager

db_client = DBSessionsManager.pg_client
logger = LoggerManager.get_psql_logger()


async def init_db():
    logger.info("Starting DB initialization")

    # Create schema

    logger.info("Start initialization of schemas")

    telegram_query = "CREATE SCHEMA IF NOT EXISTS telegram"
    users_query = "CREATE SCHEMA IF NOT EXISTS users"

    with db_client.cursor() as cursor:
        try:
            cursor.execute(telegram_query)
            cursor.execute(users_query)
        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    logger.info("End initialization of schemas")

    logger.info("Start initialization of tables")

    logger.info("Creating 'channel' table")

    channel_table_query = """
        CREATE TABLE IF NOT EXISTS telegram.channel (
            sid UUID PRIMARY KEY,
            id BIGINT NOT NULL,
            name VARCHAR NOT NULL,
            link VARCHAR NOT NULL,
            created_at DATE NOT NULL,
            is_source BOOLEAN NOT NULL
        )
    """

    with db_client.cursor() as cursor:
        try:
            cursor.execute(channel_table_query)
        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    logger.info("End creating 'channel' table")

    logger.info("Creating 'post' table")

    post_table_query = """
        CREATE TABLE IF NOT EXISTS telegram.post (
            sid UUID PRIMARY KEY,
            source_channel_sid UUID NOT NULL,
            raw_text VARCHAR NOT NULL,
            processed_text VARCHAR,
            created_at DATE NOT NULL,
            updated_at DATE,
            FOREIGN KEY (source_channel_sid) REFERENCES telegram.channel(sid)
        )
        """

    with db_client.cursor() as cursor:
        try:
            cursor.execute(post_table_query)
        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    logger.info("End creating 'post' table")

    logger.info("Creating 'publication' table")

    post_table_query = """
            CREATE TABLE IF NOT EXISTS telegram.publication (
                sid UUID PRIMARY KEY,
                target_channel_sid UUID NOT NULL,
                post_sid UUID NOT NULL,
                created_at DATE NOT NULL,
                FOREIGN KEY (target_channel_sid) REFERENCES telegram.channel(sid),
                FOREIGN KEY (post_sid) REFERENCES telegram.post(sid)
            )
            """

    with db_client.cursor() as cursor:
        try:
            cursor.execute(post_table_query)
        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    logger.info("End creating 'publication' table")

    logger.info("Creating 'media' table")

    media_table_query = """
            CREATE TABLE IF NOT EXISTS telegram.media (
                sid UUID PRIMARY KEY,
                post_sid UUID NOT NULL,
                path VARCHAR NOT NULL,
                created_at DATE NOT NULL,
                updated_at DATE,
                FOREIGN KEY (post_sid) REFERENCES telegram.post(sid)
            )
            """

    with db_client.cursor() as cursor:
        try:
            cursor.execute(media_table_query)
        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    logger.info("End creating 'media' table")

    logger.info("Creating 'user' table")

    media_table_query = """
                CREATE TABLE IF NOT EXISTS users.user (
                    sid UUID PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    id VARCHAR NOT NULL,
                    link VARCHAR NOT NULL,
                    created_at DATE NOT NULL,
                    updated_at DATE
                )
                """

    with db_client.cursor() as cursor:
        try:
            cursor.execute(media_table_query)
        except Exception as e:
            logger.error(f"{e}")
            db_client.rollback()

        db_client.commit()

    logger.info("End creating 'user' table")

    logger.info("End initialization of tables")
