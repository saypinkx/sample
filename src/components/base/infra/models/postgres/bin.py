from datetime import datetime

from src.components.base.infra.models.postgres.base import BaseModel
from sqlalchemy import DateTime, event
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class BaseBinModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()


@event.listens_for(BaseBinModel, "before_update", propagate=True)
def update_timestamp(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.utcnow()
