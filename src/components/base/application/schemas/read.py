from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class BaseReadSchema(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=False,
        populate_by_name=True,
        strict=False,
        json_encoders={
            ObjectId: str,
        },
    )

    def to_dict(self) -> dict:
        result = self.model_dump()
        return result
