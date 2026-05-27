from uuid import uuid4

from backend.src.core.mixins import AuditTrailMixin
from backend.src.model.enum import PaymentStatus, ProcessStatus, UserExaminationStatus
from sqlalchemy import UUID, Enum as SQLAlchemyEnum, Column, Date, DateTime, ForeignKey, Integer, Time

from backend.src.database.Base import base

class UserExaminationSlotClass(AuditTrailMixin, base):
    __tablename__ = "UserExaminationSlotTable"

    user_examination_slot_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    examination_slot_id = Column(UUID(as_uuid=True), ForeignKey('ExaminationSlotTable.examination_slot_id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('UserTable.user_id'))
    user_examination_status = Column(SQLAlchemyEnum(UserExaminationStatus), default=UserExaminationStatus.PENDING, nullable=False)
    payment_status = Column(SQLAlchemyEnum(PaymentStatus), default=PaymentStatus.PENDING)