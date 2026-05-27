from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.src.model.user_role import UserRoleClass
from backend.src.core.security import Security
from backend.src.exceptions import CustomException
from backend.src.model import UserClass

from sqlalchemy import UUID, select


class PromotionsRepository:

    @staticmethod
    def promote(payload, db : Session):
        try:
            if not isinstance(payload, UserRoleClass):
                new_payload = UserRoleClass(
                    user_id = payload.user_id,
                    user_role = payload.user_role,
                    updated_at = datetime.now(timezone.utc)
                )
            else:
                new_payload=payload
            db.add(new_payload)
            db.commit()
            db.refresh(new_payload)
            return f"Added {new_payload.user_role.value} as a Role for user : {new_payload.user_id}"
            
        except SQLAlchemyError as e:
            raise CustomException.RepositoryError()