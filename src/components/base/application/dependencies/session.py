from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.database.factory import async_session_factory
from src.infra.database.managers.session import AsyncSessionManager


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionManager(async_session_factory) as session:
        yield session


SessionDependency = Depends(get_session)
