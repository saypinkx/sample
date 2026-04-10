from src.infra.database.engine import engine


class database:
    @classmethod
    async def start_connection(cls):
        async with engine.begin() as conn:
            return conn
