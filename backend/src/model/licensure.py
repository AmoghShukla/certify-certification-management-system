from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, Enum as SQLAlchemyEnum, ForeignKey, Integer, Date

from backend.src.model.enum import ProcessStatus
from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base

class LicensureClass(AuditTrailMixin, base):
    __tablename__ = "LicensureTable"

    licensure_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    moc_id = Column(UUID(as_uuid=True), ForeignKey("MocTable.moc_id"))
    upload_license = Column(Boolean, default=False)
    upload_moc = Column(Boolean, default=False)
    upload_marksheet = Column(Boolean, default=False)
    licensure_status = Column(SQLAlchemyEnum(ProcessStatus), default=ProcessStatus.INCOMPLETE)
