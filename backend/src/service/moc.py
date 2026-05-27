from backend.src.repository.moc import MocRepository
from backend.src.schema import MocRequest
from backend.src.exceptions import CustomException
from backend.src.model import MocClass
from uuid import UUID

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import status
from fastapi.responses import JSONResponse

class MocService:

    @staticmethod
    def create_moc(payload : UUID , db : Session):
        moc = MocClass(cycle_id = payload.cycle_id)
        return MocRepository.create_moc(moc, db)
        
    @staticmethod
    def get_moc_by_status(moc_status, page_no : int, db : Session):
        moc =  MocRepository.get_moc_by_status(moc_status, page_no, db)
        if not moc:
            raise CustomException.NotFoundError('MOC')
        return moc
    
    @staticmethod
    def get_moc_by_cycle_id(cycle_id : UUID, db : Session):
        moc =  MocRepository.get_moc_by_cycle_id(cycle_id, db)
        if not moc:
            raise CustomException.NotFoundError(f'MOC for cycle_id : {cycle_id} ')
        return moc