from sqlalchemy import Boolean, Column, UUID, DateTime, Enum as SQLAlchemyEnum, Integer, String
from uuid import uuid4
from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base
from .enum import UserTitle
from datetime import UTC, datetime, timezone

class UserClass(AuditTrailMixin, base):
    __tablename__="UserTable"

    user_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_title = Column(SQLAlchemyEnum(UserTitle), nullable=True)
    user_first_name = Column(String, nullable=False)
    user_last_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, index=True)
    user_password = Column(String, nullable=False)
    user_degree = Column(String, nullable=True)
    user_certificate = Column(String, nullable=True)
    user_passing_year = Column(Integer, nullable=True)