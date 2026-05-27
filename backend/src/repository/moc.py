from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.src.core.config import settings
from backend.src.core.security import Security
from backend.src.exceptions import CustomException
from backend.src.model import MocClass, CycleClass, UserClass, UserRoleClass


class MocRepository:

    @staticmethod
    def create_moc(payload, db):
        try:
            if not isinstance(payload, MocClass):
                new_payload = MocClass(
                  cycle_id = payload.cycle_id   
                )
            else:
                new_payload = payload
            
            db.add(new_payload)
            db.commit()
            db.refresh(new_payload)
            return new_payload
        
        except SQLAlchemyError as e:
            raise CustomException.RepositoryError('Error While Creating MOC')

    @staticmethod
    def get_moc_by_status(moc_status, page_no, db):
            try:
                offset = (page_no - 1) * settings.LIMIT
                return db.execute(
                    select(MocClass)
                    .where(
                        MocClass.moc_status == moc_status
                    )
                    .limit(settings.LIMIT)
                    .offset(offset)
                ).scalars().all()
            except SQLAlchemyError as e:
                raise CustomException.NotFoundError(f'{moc_status} ')
    
    @staticmethod
    def get_moc_by_cycle_id(cycle_id, db):
            try:
                return db.execute(
                    select(MocClass)
                    .where(
                        MocClass.cycle_id == cycle_id
                    )
                ).scalars().all()
            except SQLAlchemyError as e:
                raise CustomException.NotFoundError(f'Not found Moc with Cycle id : {cycle_id} ')