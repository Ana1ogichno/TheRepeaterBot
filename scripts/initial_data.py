import asyncio

from src.config.db.postgres.init_db import init_db
from src.config.db.postgres.generate_date import generate_data
from src.config.db.minio.init_minio import init_s3


async def main():
    await init_db()
    await generate_data()
    await init_s3()


if __name__ == "__main__":
    asyncio.run(main())
