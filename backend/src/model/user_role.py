from sqlalchemy import Boolean, Column, UUID, DateTime, Enum as SQLAlchemyEnum, ForeignKey, Integer, String
from uuid import uuid4

from sqlalchemy.orm import Relationship
from backend.src.database.Base import base
from .enum import UserRole
from datetime import UTC, datetime, timezone
from .user import UserClass

class UserRoleClass(base):
    __tablename__="UserRoleTable"

    userrole_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = Column(UUID, ForeignKey('UserTable.user_id'), nullable=False)
    user_role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), default= lambda : datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)


