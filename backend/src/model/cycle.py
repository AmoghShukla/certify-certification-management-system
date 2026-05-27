from uuid import uuid4

from sqlalchemy import Column, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base


class CycleClass(AuditTrailMixin, base):
    __tablename__ = "CycleTable"

    cycle_id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4, 
        index=True
        )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("UserTable.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cycle_number = Column(
        Integer, 
        default=1, 
        nullable=False
        )
    start_date = Column(
        Date, 
        nullable=False, 
        index=True
        )
    end_date = Column(
        Date, 
        nullable=False, 
        index=True
        )

    user = relationship("UserClass", back_populates="cycles")
    mocs = relationship(
        "MocClass",
        back_populates="cycle",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "cycle_number", name="uq_cycle_user_number"),
    )