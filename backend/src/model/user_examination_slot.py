from uuid import uuid4

from sqlalchemy import Column, Enum as SQLAlchemyEnum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import ExaminationType, PaymentStatus, UserExaminationStatus


class UserExaminationSlotClass(AuditTrailMixin, base):
    __tablename__ = "UserExaminationSlotTable"

    user_examination_slot_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    examination_slot_id = Column(UUID(as_uuid=True), ForeignKey("ExaminationSlotTable.examination_slot_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("UserTable.user_id", ondelete="CASCADE"), nullable=False, index=True)
    examination_type = Column(SQLAlchemyEnum(ExaminationType), default=ExaminationType.ASSESSMENT, nullable=False)
    user_examination_status = Column(SQLAlchemyEnum(UserExaminationStatus), default=UserExaminationStatus.PENDING, nullable=False)
    payment_status = Column(SQLAlchemyEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)

    user = relationship("UserClass", back_populates="examination_slots")
    examination_slot = relationship("ExaminationSlotClass", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint("user_id", "examination_slot_id", name="uq_user_examination_slot"),
    )
