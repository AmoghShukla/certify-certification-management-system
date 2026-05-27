from uuid import uuid4

from sqlalchemy import Column, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.mixins import AuditTrailMixin
from src.database.Base import base
from src.model.enum import UserRole


class UserRoleClass(AuditTrailMixin, base):
    __tablename__ = "UserRoleTable"

    userrole_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("UserTable.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_role = Column(
        SQLAlchemyEnum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )

    user = relationship("UserClass", back_populates="roles")