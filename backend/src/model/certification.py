from uuid import uuid4

from sqlalchemy import Column, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import CertificationStatus


class CertificationClass(AuditTrailMixin, base):
    __tablename__ = "CertificationTable"

    certification_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4, 
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("UserTable.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    certification_status = Column(
        SQLAlchemyEnum(CertificationStatus),
        default=CertificationStatus.ACTIVE,
        nullable=False,
    )

    user = relationship("UserClass", back_populates="certifications")