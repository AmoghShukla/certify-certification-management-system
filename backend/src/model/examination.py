from uuid import uuid4

from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base


class ExaminationClass(AuditTrailMixin, base):
    __tablename__ = "ExaminationTable"

    examination_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4, 
        index=True
    )
    examination_date = Column(
        Date, 
        nullable=False, 
        index=True
        )
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("UserTable.user_id", ondelete="SET NULL"),
        nullable=True, 
        index=True,
    )

    creator = relationship(
        "UserClass",
        foreign_keys=[created_by],
        lazy="select",
    )