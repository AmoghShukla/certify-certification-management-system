from uuid import uuid4
from sqlalchemy import UUID, Column, Date, Integer, Time, Enum as SQLAlchemyEnum
from datetime import date
from backend.src.model.enum import ExaminationType
from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base

class ExaminationSlotClass(AuditTrailMixin, base):
    __tablename__ = "ExaminationSlotTable"

    examination_slot_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    examination_date = Column(Date, index=True, nullable=False)
    examination_type = Column(SQLAlchemyEnum(ExaminationType), default=ExaminationType.ASSESMENT)
    examination_slot_start_time = Column(Time, nullable=False)
    examination_slot_end_time = Column(Time, nullable=False)
    examination_slot_total_capacity = Column(Integer, default=50, nullable=False)
    examination_slot_available_capacity = Column(Integer, default=50, nullable=False)
    
