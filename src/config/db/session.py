import boto3
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

    # S3 Client
    s3_client = boto3.client(
        service_name="s3",
        endpoint_url=settings.s3.S3_URL,
        aws_access_key_id=settings.s3.S3_ACCESS_KEY,
        aws_secret_access_key=settings.s3.S3_SECRET_KEY,
        region_name=settings.s3.S3_REGION_NAME,
    )
