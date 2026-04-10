from src.infra.database.connection import database


async def startup_all() -> None:
    await database.start_connection()
    return


async def shutdown_all() -> None:
    return
