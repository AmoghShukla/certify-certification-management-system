from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime


class AuditTrailMixin:

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )
    is_deleted = Column(Boolean, default=False, nullable=False)