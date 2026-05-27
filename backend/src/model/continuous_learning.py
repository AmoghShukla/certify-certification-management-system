from uuid import uuid4

from sqlalchemy import Boolean, Column, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import ProcessStatus


class ContinuousLearningClass(AuditTrailMixin, base):
    __tablename__ = "ContinuousLearningTable"

    cl_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    moc_id = Column(
        UUID(as_uuid=True),
        ForeignKey("MocTable.moc_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    upload_proof = Column(
        Boolean, 
        default=False, 
        nullable=False
        )
    certification_proof = Column(
        Boolean, 
        default=False, 
        nullable=False
        )
    cl_status = Column(
        SQLAlchemyEnum(ProcessStatus),
        default=ProcessStatus.INCOMPLETE,
        nullable=False,
    )

    moc = relationship("MocClass", back_populates="continuous_learning")