from pydantic import BaseModel
from sqlalchemy import UUID

from src.model.enum import PaymentStatus


class BookSlotRequest(BaseModel):
    user_id: UUID
    examination_slot_id: UUID


class UpdateExaminationPaymentRequest(BaseModel):
    user_examination_slot_id: UUID
    payment_status: PaymentStatus


class TakeExaminationRequest(BaseModel):
    user_examination_slot_id: UUID


class RenewRequest(BaseModel):
    user_id: UUID


class MocPaymentToggleRequest(BaseModel):
    moc_id: UUID
    portal_payment: bool | None = None
    examination_payment: bool | None = None
    certificate_payment: bool | None = None


class LicensureToggleRequest(BaseModel):
    moc_id: UUID
    upload_license: bool | None = None
    upload_moc: bool | None = None
    upload_marksheet: bool | None = None


class ContinuousLearningToggleRequest(BaseModel):
    moc_id: UUID
    upload_proof: bool | None = None
    certification_proof: bool | None = None