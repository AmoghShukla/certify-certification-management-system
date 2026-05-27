from uuid import uuid4

from sqlalchemy import Column, Enum as SQLAlchemyEnum, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import UserTitle


class UserClass(AuditTrailMixin, base):
    __tablename__ = "UserTable"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    user_title = Column(SQLAlchemyEnum(UserTitle), nullable=True)
    user_first_name = Column(String, nullable=False)
    user_last_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True, index=True)
    user_password = Column(String, nullable=False)
    user_degree = Column(String, nullable=True)
    user_certificate = Column(String, nullable=True)
    user_passing_year = Column(Integer, nullable=True)


    roles = relationship(
        "UserRoleClass",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    cycles = relationship(
        "CycleClass",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    certifications = relationship(
        "CertificationClass",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    examination_slots = relationship(
        "UserExaminationSlotClass",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    __table_args__ = (
        UniqueConstraint("user_email", name="uq_user_email"),
    )