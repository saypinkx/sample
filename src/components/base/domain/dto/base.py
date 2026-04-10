from typing import Self

from src.components.base.infra.models.postgres.base import (
    BaseModel as BaseDatabaseModel,
)
from pydantic import ConfigDict, BaseModel


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    @classmethod
    def to_schema(cls, model: BaseDatabaseModel) -> Self:
        return cls.model_validate(model)

    def to_dict(self) -> dict:
        return self.model_dump()
