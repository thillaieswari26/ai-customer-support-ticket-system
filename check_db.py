import asyncio

from app.db.database import test_connection


asyncio.run(test_connection())