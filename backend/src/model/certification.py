from uuid import uuid4
from sqlalchemy import UUID, Column, Enum as SQLAlchemyEnum, ForeignKey

from backend.src.model.enum import CertificationStatus
from backend.src.core.mixins import AuditTrailMixin
from backend.src.database.Base import base

class CertificationClass(AuditTrailMixin, base):
    __tablename__ = "CertificationTable"

    certification_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid = True), ForeignKey('UserTable.user_id'),nullable=False, index=True)
    certification_status = Column(SQLAlchemyEnum(CertificationStatus),default=CertificationStatus.ACTIVE)