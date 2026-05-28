from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.src.schema.examination import BookSlotRequest, RenewRequest, TakeExaminationRequest, UpdateExaminationPaymentRequest
from src.database.Session import get_db
from src.model.enum import PaymentStatus
from src.service.continuous_learning_service import ContinuousLearningService
from src.service.licensure_service import LicensureService
from src.service.payment_service import ExaminationPaymentService, MocPaymentService
from src.service.renewal_service import RenewalService
from src.service.slot_booking_service import SlotBookingService
from src.service.take_examination import TakeExaminationService

router = APIRouter(prefix="/examination", tags=["Examination"])

@router.post("/book_slot")
def book_slot(payload: BookSlotRequest, db: Session = Depends(get_db)):
    return SlotBookingService.book_slot(payload.user_id, payload.examination_slot_id, db)


@router.patch("/update_payment")
def update_examination_payment(payload: UpdateExaminationPaymentRequest, db: Session = Depends(get_db)):
    return ExaminationPaymentService.update_examination_payment(
        payload.user_examination_slot_id, payload.payment_status, db
    )


@router.post("/take_examination")
def take_examination(payload: TakeExaminationRequest, db: Session = Depends(get_db)):
    return TakeExaminationService.take_examination(payload.user_examination_slot_id, db)


@router.post("/renew")
def renew_certificate(payload: RenewRequest, db: Session = Depends(get_db)):
    return RenewalService.renew_certificate(payload.user_id, db)
