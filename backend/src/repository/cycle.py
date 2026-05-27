from sqlalchemy import UUID, select
from sqlalchemy.exc import SQLAlchemyError

from backend.src.exceptions import CustomException
from backend.src.model.cycle import CycleClass


class CycleRepository:

    @staticmethod
    def create_cycle(payload, db):
        try:
            if not isinstance(payload, CycleClass):
                new_payload = CycleClass(
                    user_id = payload.user_id,
                    cycle_number = payload.cycle_number,
                    start_date = payload.start_date,
                    end_date = payload.end_date
                )
            else:
                new_payload = payload
            db.add(new_payload)
            db.commit()
            db.refresh(new_payload)
            return new_payload
        except SQLAlchemyError as e:
            raise CustomException.RepositoryError('Error while creating Cycle!!!')

    @staticmethod
    def get_cycle_by_id(cycle_id : UUID, db):
        try:   
            current_cycle = db.execute(
                select(CycleClass)
                .where(
                    CycleClass.cycle_id==cycle_id,
                    CycleClass.is_deleted==False
                )
            ).scalars().first()
            if not current_cycle:
                raise CustomException.NotFoundError(f'Cycle Id : {cycle_id}')
            return current_cycle
        except SQLAlchemyError as e: 
            raise CustomException.RepositoryError("Error While Fetching Cycle!!!")
        
    @staticmethod
    def get_cycle_by_user_id(user_id : UUID, db):
        try:   
            cycle = db.execute(
                select(CycleClass)
                .where(
                    CycleClass.user_id==user_id,
                    CycleClass.is_deleted==False
                )
            ).scalars().all()
            if not cycle:
                raise CustomException.RepositoryError("Error While Fetching Cycles!!!")
        except SQLAlchemyError as e: 
            raise CustomException.RepositoryError("Error While Fetching all Cycles for the user!!!")

