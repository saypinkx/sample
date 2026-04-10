from typing import Generic, TypeVar

from src.components.base.domain.dto.base import BaseDTO
from src.components.base.infra.repositories.interface import BaseInterfaceRepository

T = TypeVar("T", bound=BaseDTO)


class BaseService(Generic[T]):
    _repository: BaseInterfaceRepository[T]

    def __init__(self, repository: BaseInterfaceRepository):
        self._repository = repository

    async def create(self, **kwargs) -> T:
        return await self._repository.create(**kwargs)

    async def update(self, instance_id: int, *args, **kwargs) -> T:
        return await self._repository.update(instance_id, **kwargs)

    async def delete(self, instance_id: int) -> None:
        return await self._repository.delete(instance_id)

    async def get(self, instance_id: int) -> T:
        return await self._repository.get(instance_id)
