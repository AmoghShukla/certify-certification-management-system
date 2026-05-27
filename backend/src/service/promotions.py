from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from backend.src.model.enum import UserRole
from backend.src.model.user_role import UserRoleClass
from backend.src.repository.promotions import PromotionsRepository
from backend.src.repository.user_role import UserRoleRepository
from backend.src.model.user import UserClass
from backend.src.exceptions import CustomException
from backend.src.repository.user import UserRepository

from sqlalchemy.orm import Session

from datetime import datetime, timezone
from fastapi import status
from fastapi.responses import JSONResponse

class PromotionsService:

    @staticmethod
    def verify_not_admin(current_role):
        if current_role.user_role in (UserRole.ADMIN, UserRole.SUPERADMIN):
            raise CustomException.BadRequestError("User is Already an ADMIN!!")

    @staticmethod
    def promote_to_admin(email_id, db):
        user = UserRepository.get_user_by_email_id(email_id, db)
        if not user:
            raise CustomException.UserNotFoundError()
        
        roles = UserRoleRepository.get_user_role_by_user_id(user.user_id, db)
        if not roles:
            raise CustomException.UserRoleNotFoundError()  

        for current_role in roles:
            PromotionsService.verify_not_admin(current_role)
        
        role_payload = UserRoleClass(
            user_id = user.user_id,
            user_role = UserRole.ADMIN,
            updated_at = datetime.now(timezone.utc)
        )
        
        promotion = PromotionsRepository.promote(role_payload, db)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=promotion
        )
