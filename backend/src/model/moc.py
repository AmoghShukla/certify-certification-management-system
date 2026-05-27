from uuid import uuid4

from sqlalchemy import Column, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import MocStatus


class MocClass(AuditTrailMixin, base):
    __tablename__ = "MocTable"

    moc_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4, 
        index=True
        )
    cycle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("CycleTable.cycle_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    moc_status = Column(
        SQLAlchemyEnum(MocStatus),
        default=MocStatus.INCOMPLETE,
        nullable=False,
    )

    cycle = relationship("CycleClass", back_populates="mocs")

    payment = relationship(
        "PaymentClass",
        back_populates="moc",
        uselist=False,         
        cascade="all, delete-orphan",
        lazy="select",
    )
    licensure = relationship(
        "LicensureClass",
        back_populates="moc",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",
    )
    continuous_learning = relationship(
        "ContinuousLearningClass",
        back_populates="moc",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",
    )