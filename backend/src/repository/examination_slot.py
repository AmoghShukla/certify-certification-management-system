from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import UUID, select

from backend.src.core.config import settings
from backend.src.model.slot import ExaminationSlotClass
from backend.src.core.security import Security
from backend.src.exceptions import CustomException

class ExaminationSlotRepository:

    @staticmethod
    def create_examination(payload : ExaminationSlotClass, db):
        try:
            if isinstance(payload, ExaminationSlotClass):
                new_payload = payload
            else:
                new_payload = ExaminationSlotClass(
                    examination_date = payload.examination_date,
                    examination_type = payload.examination_type,
                    examination_slot_start_time = payload.examination_slot_start_time,
                    examination_slot_end_time = payload.examination_slot_end_time,
                    examination_slot_total_capacity = payload.examination_slot_total_capacity,
                    examination_slot_available_capacity = payload.examination_slot_total_capacity

                )
            db.add(new_payload)
            db.commit()
            db.refresh(new_payload)
            return new_payload
        except SQLAlchemyError as e:
            db.rollback()
            raise CustomException.BadRequestError('Error While Scheduling Examination')

    @staticmethod
    def get_examination_by_date(page_no : int, date, db : Session):
        try:
            offset = (page_no - 1) * settings.LIMIT
            return db.execute(
                select(ExaminationSlotClass).
                where(
                    ExaminationSlotClass.examination_date==date
                )
                .limit(settings.LIMIT)
                .offset(offset)
            ).scalars().first()
        except SQLAlchemyError:
            raise CustomException.BadRequestError()
        
    @staticmethod
    def get_examination_by_type(page_no : int, exmination_type ,  db : Session):
        try:
            limit = 5
            offset = (page_no - 1) * limit
            return db.execute(
                select(ExaminationSlotClass).
                where(
                    ExaminationSlotClass.examination_type==exmination_type
                )
                .limit(limit)
                .offset(offset)    
            ).scalars().all()
        except SQLAlchemyError as e:
            raise CustomException.BadRequestError('No Examinations Exist!!!')
    
    @staticmethod
    def get_examination(payload, db : Session):
        try:
            return db.execute(
                select(ExaminationSlotClass).
                where(
                    ExaminationSlotClass.examination_date==payload.examination_date,
                    ExaminationSlotClass.examination_slot_end_time > payload.examination_slot_start_time
                )   
            ).scalars().first()
        except SQLAlchemyError as e:
            raise CustomException.BadRequestError('No Examinations Exist!!!')
        
    @staticmethod
    def get_examination_by_slot(payload, db : Session):
        try:
            return db.execute(
                select(ExaminationSlotClass).
                where(
                    ExaminationSlotClass.examination_date==payload.examination_date,
                    ExaminationSlotClass.examination_slot_start_time==payload.examination_slot_start_time,
                    ExaminationSlotClass.examination_slot_end_time == payload.examination_slot_end_time
                )   
            ).scalars().first()
        except SQLAlchemyError as e:
            raise CustomException.BadRequestError('No Examinations Exist!!!')     
    
    @staticmethod
    def get_all_examinations(page_no : int, db):
        try:
            offset = (page_no - 1) * settings.LIMIT

            return db.execute(
                select(ExaminationSlotClass)
                .limit(settings.LIMIT)
                .offset(offset)
            ).scalars().all()
        except SQLAlchemyError as e:
            raise CustomException.BadRequestError()