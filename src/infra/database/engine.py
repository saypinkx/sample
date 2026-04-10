from src.config import POSTGRES_URL
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    POSTGRES_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_timeout=30,
)
