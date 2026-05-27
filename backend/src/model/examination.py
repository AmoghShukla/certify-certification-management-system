from uuid import uuid4
from sqlalchemy import UUID, Column, Date, Enum as SQLAlchemyEnum

from backend.src.core.mixins import AuditTrailMixin
from backend.src.model.enum import ExaminationType
from backend.src.database.Base import base

class ExaminationClass(AuditTrailMixin, base):
    __tablename__ = "ExaminationTable"

    examination_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    examination_date = Column(Date, nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), nullable=False, index=True)

