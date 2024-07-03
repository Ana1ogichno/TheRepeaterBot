from psycopg2 import connect

from src.config.settings import settings


class DBSessionsManager:
    """Class for storage DB's clients"""

    # Postgres Client
    pg_client = connect(
        database=settings.pg_settings.POSTGRES_DB,
        user=settings.pg_settings.POSTGRES_USER,
        password=settings.pg_settings.POSTGRES_PASSWORD,
        host=settings.pg_settings.POSTGRES_HOST,
        port=settings.pg_settings.POSTGRES_PORT,
    )
