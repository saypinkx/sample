from src.components.base.application.schemas.abstract import AbstractSchema
from pydantic import ConfigDict


class BasePayloadSchema(AbstractSchema):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        strict=False,
        from_attributes=True,
    )

    def to_dict(self) -> dict:
        result = self.model_dump()  # json
        return result
