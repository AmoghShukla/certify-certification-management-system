from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, Date, Enum as SQLAlchemyEnum, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import ExaminationType


class ExaminationSlotClass(AuditTrailMixin, base):
    __tablename__ = "ExaminationSlotTable"

    examination_slot_id = Column(
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
    examination_type = Column(
        SQLAlchemyEnum(ExaminationType),
        default=ExaminationType.ASSESSMENT,
        nullable=False,
    )
    examination_slot_start_time = Column(
        Time, 
        nullable=False
        )
    examination_slot_end_time = Column(
        Time, 
        nullable=False
        )
    examination_slot_total_capacity = Column(
        Integer, 
        default=50, 
        nullable=False
        )
    examination_slot_available_capacity = Column(
        Integer, 
        default=50, 
        nullable=False
        )
    bookings = relationship(
        "UserExaminationSlotClass",
        back_populates="examination_slot",
        cascade="all, delete-orphan",
        lazy="select",
    )

    __table_args__ = (
        CheckConstraint(
            "examination_slot_available_capacity >= 0"
            " AND examination_slot_available_capacity <= examination_slot_total_capacity",
            name="ck_slot_capacity_bounds",
        ),
    )