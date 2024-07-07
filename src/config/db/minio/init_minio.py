from src.common.logger import LoggerManager
from src.config.db import DBSessionsManager
from src.config.settings import settings


s3_client = DBSessionsManager.s3_client
s3_logger = LoggerManager.get_s3_logger()


async def init_s3() -> None:
    """Function to initialize s3 storage"""

    s3_logger.info("Start creating bucket")

    buckets = [settings.s3.MEDIA_BUCKET_NAME]
    response = s3_client.list_buckets()
    for bucket in buckets:
        need_create = True
        for exist_bucket in response["Buckets"]:
            if bucket == exist_bucket["Name"]:
                need_create = False
        if need_create:
            s3_client.create_bucket(Bucket=bucket)

    s3_logger.info("End creating bucket")
