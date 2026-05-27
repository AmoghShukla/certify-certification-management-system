from datetime import datetime, timezone

# from pydantic_ai import settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.src.core.security import Security
from backend.src.exceptions import CustomException
from backend.src.model import UserClass
from backend.src.core.config import settings

from sqlalchemy import UUID, select


class UserRepository:

    @staticmethod
    def create_admin(payload , db : Session):
        try:
            current_password = Security.hash_password(payload.user_password)
            new_user = UserClass(
                user_title = payload.user_title,
                user_first_name = payload.user_first_name,
                user_last_name = payload.user_last_name,
                user_email = payload.user_email,
                user_password = current_password,
                user_degree = payload.user_degree,
                user_certificate = payload.user_certificate,
                user_passing_year = payload.user_passing_year,
                updated_at = datetime.now(timezone.utc)
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            db.rollback()
            raise CustomException.RepositoryError('Error while Creating User!!!')

    @staticmethod
    def get_user_by_user_id(
        user_id : UUID,
        db : Session
        ):
        try:
            query = select(UserClass).where(
                UserClass.user_id==user_id
            )
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:            
            raise CustomException.RepositoryError("Error While Fetching user with user-id!!")

    @staticmethod
    def get_user_by_email_id(
        user_email_id, 
        db : Session
        ):
        try:
            query = select(UserClass).where(
                UserClass.user_email==user_email_id
            )
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:
            raise CustomException.RepositoryError("Error While Fetching user with email-id!!")
    
    @staticmethod
    def get_all_user(page_no: int, db : Session):
        try:
            offset = (page_no - 1) * settings.LIMIT
            return db.execute(select(UserClass).limit(settings.LIMIT).offset(offset)).scalars().all()
        except SQLAlchemyError as e:
            raise CustomException.UserNotFoundError()
        