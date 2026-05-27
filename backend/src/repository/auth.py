from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from backend.src.exceptions import CustomException

from ..schema import RegisterUser
from ..model import UserClass
from backend.src.core.security import Security

class AuthRepository:

    @staticmethod
    def register_user(payload , db):
        try:
            if isinstance(payload, UserClass):
                new_user = payload
            else:
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
            raise CustomException.RepositoryError('Error while Creating User!!!')