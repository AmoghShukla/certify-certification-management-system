from uuid import uuid4

from sqlalchemy import Column, Date, Enum as SQLAlchemyEnum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import CertificationStatus


class CertificationClass(AuditTrailMixin, base):
    __tablename__ = "CertificationTable"

    certification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("UserTable.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_examination_slot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("UserExaminationSlotTable.user_examination_slot_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    certification_number = Column(
        String, 
        unique=True, 
        nullable=True
        )  
    issued_date = Column(
        Date, 
        nullable=False
        )
    valid_until = Column(
        Date, 
        nullable=False
        )           
    renewal_count = Column(
        Integer, 
        default=0, 
        nullable=False
        )  
    certification_status = Column(
        SQLAlchemyEnum(CertificationStatus),
        default=CertificationStatus.ACTIVE,
        nullable=False,
    )

    user = relationship("UserClass", back_populates="certifications")
    cycles = relationship("CycleClass", back_populates="certification", cascade="all, delete-orphan")
