from uuid import uuid4
from sqlalchemy import UUID, Column, Enum as SQLAlchemyEnum, ForeignKey, Integer, Date

from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base
from backend.src.model.enum import MocStatus


class MocClass(AuditTrailMixin, base):
    __tablename__ = "MocTable"

    moc_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    cycle_id = Column(UUID(as_uuid=True), ForeignKey("CycleTable.cycle_id"))
    moc_status = Column(SQLAlchemyEnum(MocStatus), default=MocStatus.INCOMPLETE)

