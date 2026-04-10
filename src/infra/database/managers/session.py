from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AsyncSessionManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self) -> AsyncSession:
        self.session = self._session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                if self.session.dirty or self.session.new or self.session.deleted:
                    await self.session.commit()
        finally:
            await self.session.close()
