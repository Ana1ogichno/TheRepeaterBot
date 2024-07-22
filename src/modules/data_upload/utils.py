from src.common.logger import LoggerManager
from src.config.db import DBSessionsManager
from src.common import logging_call


class DataUploadUtils:
    def __init__(self):
        self._db_client = DBSessionsManager.pg_client
        self._psql_logger = LoggerManager.get_psql_logger()
        self._s3_client = DBSessionsManager.s3_client
        self._s3_logger = LoggerManager.get_s3_logger()

    @logging_call()
    async def execute_query_with_result(self, query: str):
        with self._db_client.cursor() as cursor:
            try:
                cursor.execute(query)
                return cursor.fetchall()

            except Exception as e:
                self._psql_logger.error(f"{e}")
                self._db_client.rollback()

        return False

    @logging_call()
    async def execute_query(self, query: str):
        with self._db_client.cursor() as cursor:
            try:
                cursor.execute(query)
                self._db_client.commit()

            except Exception as e:
                self._psql_logger.error(f"{e}")
                self._db_client.rollback()

        return False

    @logging_call()
    async def upload_to_s3(self, *, path_to_file: str, bucket: str, path_in_s3: str):
        try:
            self._s3_client.upload_file(path_to_file, bucket, path_in_s3)
        except Exception as e:
            self._s3_logger.error(f"{e}")
