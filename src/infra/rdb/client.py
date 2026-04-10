from redis import asyncio as aioredis
from src.config import (
    REDIS_HOST,
    REDIS_KEY_STORAGE_DB,
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_TRACEBACK_STORAGE_DB,
)

rdb = aioredis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_KEY_STORAGE_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)
rdb_traceback = aioredis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_TRACEBACK_STORAGE_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)
