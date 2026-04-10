from sqlalchemy.ext.asyncio import async_sessionmaker
from src.infra.database.engine import engine

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
