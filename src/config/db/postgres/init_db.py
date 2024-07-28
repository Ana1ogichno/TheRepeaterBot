from src.modules.data_upload.data_upload import DataUploadUtils
from src.common.logger import LoggerManager

_logger = LoggerManager.get_psql_logger()
_data_upload_utils = DataUploadUtils()


async def init_db():
    _logger.info("Starting DB initialization")

    _logger.info("Start initialization of schemas")
    telegram_query = "CREATE SCHEMA IF NOT EXISTS telegram"
    users_query = "CREATE SCHEMA IF NOT EXISTS users"
    await _data_upload_utils.execute_query(telegram_query)
    await _data_upload_utils.execute_query(users_query)
    _logger.info("End initialization of schemas")

    _logger.info("Start initialization of tables")
    _logger.info("Creating 'channel' table")
    channel_table_query = """
        CREATE TABLE IF NOT EXISTS telegram.channel (
            sid UUID PRIMARY KEY,
            id BIGINT NOT NULL,
            name VARCHAR NOT NULL,
            link VARCHAR NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            is_source BOOLEAN NOT NULL
        )
    """
    await _data_upload_utils.execute_query(channel_table_query)
    _logger.info("End creating 'channel' table")

    _logger.info("Creating 'post' table")
    post_table_query = """
        CREATE TABLE IF NOT EXISTS telegram.post (
            sid UUID PRIMARY KEY,
            source_channel_sid UUID NOT NULL,
            raw_text VARCHAR,
            processed_text VARCHAR,
            grouped_id BIGINT,
            is_viewed BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITHOUT TIME ZONE,
            FOREIGN KEY (source_channel_sid) REFERENCES telegram.channel(sid)
        )
        """
    await _data_upload_utils.execute_query(post_table_query)
    _logger.info("End creating 'post' table")

    _logger.info("Creating 'publication' table")
    publication_table_query = """
            CREATE TABLE IF NOT EXISTS telegram.publication (
                sid UUID PRIMARY KEY,
                target_channel_sid UUID NOT NULL,
                post_sid UUID NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                FOREIGN KEY (target_channel_sid) REFERENCES telegram.channel(sid),
                FOREIGN KEY (post_sid) REFERENCES telegram.post(sid)
            )
            """
    await _data_upload_utils.execute_query(publication_table_query)
    _logger.info("End creating 'publication' table")

    _logger.info("Creating 'media' table")
    media_table_query = """
            CREATE TABLE IF NOT EXISTS telegram.media (
                sid UUID PRIMARY KEY,
                post_sid UUID NOT NULL,
                path VARCHAR NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                updated_at TIMESTAMP WITHOUT TIME ZONE,
                FOREIGN KEY (post_sid) REFERENCES telegram.post(sid)
            )
            """
    await _data_upload_utils.execute_query(media_table_query)
    _logger.info("End creating 'media' table")

    _logger.info("Creating 'user' table")
    user_table_query = """
                CREATE TABLE IF NOT EXISTS users.user (
                    sid UUID PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    id VARCHAR NOT NULL,
                    link VARCHAR NOT NULL,
                    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITHOUT TIME ZONE
                )
                """
    await _data_upload_utils.execute_query(user_table_query)
    _logger.info("End creating 'user' table")

    _logger.info("End initialization of tables")
