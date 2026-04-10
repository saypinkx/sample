from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from src.components.base.domain.dto.base import BaseDTO

T = TypeVar("T", bound=BaseDTO)

class BaseInterfaceRepository(ABC, Generic[T]):
    _dto_type: type[T]

    @abstractmethod
    def __init__(self, session: Any): ...

    @abstractmethod
    async def create(self, **kwargs) -> T: ...

    @abstractmethod
    async def update(self, instance: Any, *args, **kwargs) -> T: ...

    @abstractmethod
    async def delete(self, instance: Any) -> None: ...

    @abstractmethod
    async def get(self, instance_id: Any) -> T: ...
