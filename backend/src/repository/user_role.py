from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from src.exceptions import CustomException
from src.model import UserRoleClass
 
 
class UserRoleRepository:
 
    @staticmethod
    def register_role(payload, db):
        try:
            if not isinstance(payload, UserRoleClass):
                new_payload = UserRoleClass(
                    user_id=payload.user_id,
                    user_role=payload.user_role,
                )
            else:
                new_payload = payload
            db.add(new_payload)
            db.commit()
            db.refresh(new_payload)
            return new_payload
        except SQLAlchemyError:
            db.rollback()
            raise CustomException.RepositoryError(
                f"Error while registering role for user_id: {payload.user_id}"
            )
 
    @staticmethod
    def get_all_roles_by_user_id(user_id, db) -> list:
        try:
            return db.execute(
                select(UserRoleClass).where(
                    UserRoleClass.user_id == user_id,
                    UserRoleClass.is_deleted == False,   # noqa: E712
                )
            ).scalars().all()
        except SQLAlchemyError:
            raise CustomException.UserNotFoundError()
 
    @staticmethod
    def get_user_role_by_user_id_single(user_id, db):
        try:
            return db.execute(
                select(UserRoleClass).where(
                    UserRoleClass.user_id == user_id,
                    UserRoleClass.is_deleted == False,   # noqa: E712
                )
            ).scalars().first()
        except SQLAlchemyError:
            raise CustomException.UserNotFoundError()
 
    @staticmethod
    def get_user_by_role(query, db):
        try:
            return db.execute(query).scalars().all()
        except SQLAlchemyError:
            raise CustomException.UserRoleNotFoundError()
 
    @staticmethod
    def get(query, db):
        return db.execute(query).scalars().all()
