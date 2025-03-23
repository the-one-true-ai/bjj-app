from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql import func

@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


@declarative_mixin
class PIIMixin:
    """Mixin to tag PII fields dynamically."""
    def get_pii_fields(self):
        return [
            col.name
            for col in self.__table__.columns
            if col.info.get("is_pii", False)
        ]
