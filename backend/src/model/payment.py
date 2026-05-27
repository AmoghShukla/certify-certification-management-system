from uuid import uuid4

from sqlalchemy import Boolean, Column, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import PaymentStatus, ProcessStatus


class PaymentClass(AuditTrailMixin, base):
    __tablename__ = "PaymentTable"

    payment_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4, 
        index=True
    )
    moc_id = Column(
        UUID(as_uuid=True),
        ForeignKey("MocTable.moc_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    portal_payment_status = Column(
        Boolean, 
        default=False, 
        nullable=False
        )
    examination_payment_status = Column(
        Boolean, 
        default=False, 
        nullable=False
        )
    certificate_payment_status = Column(
        Boolean, 
        default=False, 
        nullable=False
        )
    payment_status = Column(
        SQLAlchemyEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    moc = relationship("MocClass", back_populates="payment")