from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, Enum as SQLAlchemyEnum, ForeignKey, Integer, Date

from backend.src.model.enum import ProcessStatus
from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base

class PaymentClass(AuditTrailMixin, base):
    __tablename__ = "PaymentTable"

    payment_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    moc_id = Column(UUID(as_uuid=True), ForeignKey("MocTable.moc_id"))
    portal_payment_status = Column(Boolean, default=False)
    examination_payment_status = Column(Boolean, default=False)
    certificate_payment_status = Column(Boolean, default=False)
    payment_status = Column(SQLAlchemyEnum(ProcessStatus), default=ProcessStatus.INCOMPLETE)