from fastapi import APIRouter, Depends
from backend.src.model.enum import ExaminationType
from backend.src.schema.examination_slot import ExaminationCreate, ExaminationResponse
from sqlalchemy.orm import Session

from backend.src.service.examination_slot import ExaminationService
from backend.src.database.Session import get_db


router = APIRouter(prefix='/examination', tags=['Examination'])

@router.post('/create_examination', response_model=ExaminationResponse)
def create_examination(payload : ExaminationCreate, db : Session = Depends(get_db)):
    return ExaminationService.create_examination(payload, db)

@router.get('/get_all_examinations', response_model=list[ExaminationResponse])
def get_all_examinations(page_no : int, db : Session = Depends(get_db)):
    return ExaminationService.get_all_examinations(page_no, db)

@router.get('/get_examination_by_type', response_model=list[ExaminationResponse])
def get_examination_by_type(page_no : int, examination_type : ExaminationType,db : Session = Depends(get_db)):
    return ExaminationService.get_examinations_by_type(page_no, examination_type, db)
