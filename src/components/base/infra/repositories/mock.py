from datetime import datetime
from typing import Any, Generic, TypeVar

from src.components.base.domain.dto.base import BaseDTO
from src.components.base.infra.repositories.interface import BaseInterfaceRepository

T = TypeVar("T", bound=BaseDTO)

class BaseMockRepository(BaseInterfaceRepository[T], Generic[T]):
    _dto_type: type[T]

    def __init__(self, session: Any = None):
        self._storage: dict[int, T] = {}
        self._next_id = 1

    async def create(self, **kwargs) -> T:
        data = {
            "id": self._next_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            **kwargs,
        }
        instance = self._dto_type(**data)
        self._storage[self._next_id] = instance
        self._next_id += 1
        return instance

    async def get(self, instance_id: int) -> T:
        if instance_id not in self._storage:
            raise Exception(
                f"{self._dto_type.__name__} with id {instance_id} not found"
            )
        return self._storage[instance_id]

    async def update(self, instance: T, **kwargs) -> T:
        current_data = instance.to_dict()
        updated_data = {**current_data, **kwargs, "updated_at": datetime.utcnow()}
        updated_instance = self._dto_type(**updated_data)
        if hasattr(instance, "id") and instance.id in self._storage:
            self._storage[instance.id] = updated_instance
        return updated_instance

    async def delete(self, instance: T) -> None:
        if hasattr(instance, "id") and instance.id in self._storage:
            del self._storage[instance.id]
        return None

    def clear(self) -> None:
        self._storage.clear()
        self._next_id = 1
