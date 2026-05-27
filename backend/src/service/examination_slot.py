
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.src.model.slot import ExaminationSlotClass
from backend.src.exceptions import CustomException
from backend.src.repository.examination_slot import ExaminationSlotRepository
from backend.src.model.examination import ExaminationClass


class ExaminationService:

    @staticmethod
    def create_examination(payload, db : Session):
        exam = ExaminationSlotRepository.get_examination(payload, db)
        if exam:
            raise CustomException.AlreadyExistsError("Examination in this Slot ")

        new_payload = ExaminationSlotClass(
                examination_date = payload.examination_date,
                examination_type = payload.examination_type,
                examination_slot_start_time = payload.examination_slot_start_time,
                examination_slot_end_time = payload.examination_slot_end_time,
                examination_slot_total_capacity = payload.examination_slot_total_capacity,
                examination_slot_available_capacity = payload.examination_slot_total_capacity,
                updated_at = datetime.now(timezone.utc)
            )
        
        return ExaminationSlotRepository.create_examination(new_payload, db)
    
    @staticmethod
    def get_examination_by_date(page_no, date , db : Session):
        examination_by_date = ExaminationSlotRepository.get_examination_by_date(page_no, date, db)

        if not examination_by_date:
            raise CustomException.NotFoundError('Examination')
        
    @staticmethod
    def get_all_examinations(page_no : int, db : Session):
        return ExaminationSlotRepository.get_all_examinations(page_no, db)
    
    @staticmethod
    def get_examinations_by_type(page_no : int, examination_type : str, db : Session):
        return ExaminationSlotRepository.get_examination_by_type(page_no, examination_type, db)