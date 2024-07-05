import asyncio
import sys

sys.path = ["", ".."] + sys.path[1:]

from src.config.db.postgres.init_db import init_db


if __name__ == "__main__":
    asyncio.run(init_db())
