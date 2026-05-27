from uuid import uuid4
from sqlalchemy import UUID, Column, Enum as SQLAlchemyEnum, ForeignKey, Integer, Date

from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base

class CycleClass(AuditTrailMixin, base):
    __tablename__ = "CycleTable"

    cycle_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("UserTable.user_id"))
    cycle_number = Column(Integer, default=1, nullable=False)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)