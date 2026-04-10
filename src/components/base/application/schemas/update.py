from src.components.base.application.schemas.abstract import AbstractSchema
from pydantic import ConfigDict


class BaseUpdateSchema(AbstractSchema):
    model_config = ConfigDict(
        arbitrary_types_allowed=False,
        populate_by_name=True,
        strict=False,
    )

    def to_dict(self) -> dict:
        result = self.model_dump(exclude_unset=True)
        return result
