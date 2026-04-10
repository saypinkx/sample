from datetime import datetime
from typing import Generic, TypeVar

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from src.components.base.domain.dto.base import BaseDTO
from src.components.base.infra.exceptions.not_found import EntityNotFound
from src.components.base.infra.models.postgres.base import BaseModel
from src.components.base.infra.repositories.interface import BaseInterfaceRepository

T = TypeVar("T", bound=BaseDTO)


class BasePostgresRepository(BaseInterfaceRepository[T], Generic[T]):
    _session: AsyncSession
    _model_type: type[BaseModel]
    _dto_type: type[T]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, *args, **kwargs) -> T:
        instance = self._model_type(**kwargs)
        self._session.add(instance)
        await self._session.flush()
        return self._dto_type.to_schema(instance)

    async def _get(self, instance_id: int) -> BaseModel:
        stmt = select(self._model_type).where(
            self._model_type.id == instance_id,
        )
        node = await self._session.execute(stmt)
        result = node.scalar()
        if not result:
            raise EntityNotFound(f"{self._model_type.name()} with id not found")
        return result

    async def delete(self, instance: T) -> None:
        stmt = sql_update(self._model_type).where(
            self._model_type.id == instance.id
        ).values(deleted_at=datetime.now())
        await self._session.execute(stmt)
        return None

    async def _hard_delete(self, instance: T) -> None:
        stmt = sql_delete(self._model_type).where(
            self._model_type.id == instance.id
        )
        await self._session.execute(stmt)
        return None

    async def update(self, instance: T, *args, **kwargs) -> T:
        stmt = sql_update(self._model_type).where(
            self._model_type.id == instance.id
        ).values(**kwargs).returning(self._model_type)
        result = await self._session.execute(stmt)
        updated_model = result.scalar_one()
        return self._dto_type.to_schema(updated_model)

    async def get(self, instance_id: int) -> T:
        document = await self._get(instance_id)
        return self._dto_type.to_schema(document)
