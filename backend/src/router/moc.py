from fastapi import APIRouter, Depends
from backend.src.model.enum import MocStatus
from backend.src.schema import MocResponse, MocRequest
from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.schema.examination import LicensureToggleRequest
from backend.src.service.licensure_service import LicensureService
from backend.src.service.moc import MocService
from backend.src.database.Session import get_db


router = APIRouter(prefix='/maintenance_of_certificate', tags=['Moc'])

@router.post('/create_moc', response_model=MocResponse)
def create_moc(cycle_id : UUID, db : Session = Depends(get_db)):
    return MocService.create_moc(cycle_id, db)

@router.get('/get_user_by_moc_status', response_model=list[MocResponse])
def get_moc_by_status(moc_status : MocStatus, page_no : int, db : Session = Depends(get_db)):
    return MocService.get_moc_by_status(moc_status, page_no, db)

@router.patch("/moc/payment")
def toggle_moc_payment(payload: MocPaymentToggleRequest, db: Session = Depends(get_db)):
    return MocPaymentService.toggle_moc_payment_item(
        payload.moc_id,
        payload.portal_payment,
        payload.examination_payment,
        payload.certificate_payment,
        db,
    )


@router.patch("/moc/licensure")
def toggle_licensure(payload: LicensureToggleRequest, db: Session = Depends(get_db)):
    return LicensureService.toggle_licensure(
        payload.moc_id,
        payload.upload_license,
        payload.upload_moc,
        payload.upload_marksheet,
        db,
    )


@router.patch("/moc/continuous_learning")
def toggle_continuous_learning(payload: ContinuousLearningToggleRequest, db: Session = Depends(get_db)):
    return ContinuousLearningService.toggle_continuous_learning(
        payload.moc_id,
        payload.upload_proof,
        payload.certification_proof,
        db,
    )
