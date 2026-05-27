from fastapi import APIRouter, Depends
from backend.src.model.enum import MocStatus
from backend.src.schema import MocResponse, MocRequest
from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.service.moc import MocService
from backend.src.database.Session import get_db


router = APIRouter(prefix='/maintenance_of_certificate', tags=['Moc'])

@router.post('/create_moc', response_model=MocResponse)
def create_moc(cycle_id : UUID, db : Session = Depends(get_db)):
    return MocService.create_moc(cycle_id, db)

@router.get('/get_user_by_moc_status', response_model=list[MocResponse])
def get_moc_by_status(moc_status : MocStatus, page_no : int, db : Session = Depends(get_db)):
    return MocService.get_moc_by_status(moc_status, page_no, db)