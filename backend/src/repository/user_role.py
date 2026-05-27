from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from backend.src.exceptions import CustomException
from backend.src.model import UserRoleClass

class UserRoleRepository:

    @staticmethod
    def register_role(Payload, db):
        try:
            if not isinstance(Payload, UserRoleClass):
                new_payload = UserRoleClass(
                    user_id = Payload.user_id,
                    user_role = Payload.user_role,
                    updated_at = datetime.now(timezone.utc)
                )
            else:
                new_payload=Payload
            db.add(new_payload)
            db.commit()
            db.refresh(new_payload)
            return new_payload
        except SQLAlchemyError as e:
            db.rollback()
            raise CustomException.RepositoryError(f"Error while Registering Role for user_id : {Payload.user_id}")
        
    def get_user_role_by_user_id_single(user_id, db):
        try:
            return db.execute(
                select(UserRoleClass)
                .where(
                    UserRoleClass.user_id==user_id
                )
            ).scalars().first()
        except SQLAlchemyError as e:
            raise CustomException.UserNotFoundError()
    
    def get_user_role_by_user_id(user_id, db):
        try:
            return db.execute(
                select(UserRoleClass)
                .where(
                    UserRoleClass.user_id==user_id
                )
            ).scalars().all()
        except SQLAlchemyError as e:
            raise CustomException.UserNotFoundError()
        
    def get_user_by_role(query, db):
        try:
            return db.execute(query).scalars().all()
        except SQLAlchemyError as e:
            raise CustomException.UserRoleNotFoundError()
        
    @staticmethod
    def get(query, db):
        return db.execute(query).scalars().all()