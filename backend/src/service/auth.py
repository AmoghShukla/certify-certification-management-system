import os
from datetime import datetime, timezone
 
from sqlalchemy.orm import Session
 
from src.core.security import Security
from src.exceptions import CustomException
from src.model.enum import UserRole, highest_role
from src.model.user_role import UserRoleClass
from src.repository.auth import AuthRepository
from src.repository.user import UserRepository
from src.repository.user_role import UserRoleRepository
from src.schema import UserResponse
from src.service.aws_s3_service import S3Service
from src.service.email_service import send_email
from src.router.user import get_admin
 
 
class AuthService:
 
    @staticmethod
    def register_user(payload, background_tasks, db):
        try:
            user = UserRepository.get_user_by_email_id(payload.user_email, db)
            if user:
                raise CustomException.UserAlreadyExists()
            if payload.user_password != payload.user_confirm_password:
                raise CustomException.PasswordDoesNotMatch()
 
            if payload.user_certificate is not None:
                uploaded_certificate = S3Service.upload_file(payload.user_certificate)
                if not uploaded_certificate:
                    raise CustomException.ServiceError("Error while uploading user certificate!")
                payload.user_certificate = uploaded_certificate
 
            if not os.path.exists("src/utils/temps"):
                os.makedirs("src/utils/temps", exist_ok=True)
 
            created_user = AuthRepository.register_user(payload, db)
            if not created_user:
                raise CustomException.BadRequestError()
 
            role_payload = UserRoleClass(
                user_id=created_user.user_id,
                user_role=UserRole.USER,
            )
            created_role = UserRoleRepository.register_role(role_payload, db)
 
            admins = get_admin(db)
            admin_emails = [admin.user_email for admin in admins]
            background_tasks.add_task(
                send_email,
                admin_emails,
                "User Registration Mail",
                f"{payload.user_first_name} has been onboarded onto our application",
            )
 
            return UserResponse(
                user_id=created_user.user_id,
                user_title=created_user.user_title,
                user_first_name=created_user.user_first_name,
                user_last_name=created_user.user_last_name,
                user_email=created_user.user_email,
                user_role=created_role.user_role,
                user_degree=created_user.user_degree,
                user_passing_year=created_user.user_passing_year,
                updated_at=created_user.updated_at,
            )
        except CustomException.RepositoryError as e:
            raise CustomException.ServiceError(str(e))
 

    @staticmethod
    def login_user(payload, db: Session):
        user = UserRepository.get_user_by_email_id(payload.username, db)
        if not user:
            raise CustomException.UserNotFoundError(
                "User does not exist — please register first."
            )
 
        if not Security.verify_password(payload.password, user.user_password):
            raise CustomException.PasswordDoesNotMatchError()
 
        role_rows = UserRoleRepository.get_all_roles_by_user_id(user.user_id, db)
        if not role_rows:
            raise CustomException.ServiceError("No role assigned to this user.")
 
        roles: list[str] = [row.user_role.value for row in role_rows]
        top_role: str = highest_role(roles) 
 
        token_payload = {
            "sub": str(user.user_id),
            "roles": roles,          # ["ADMIN", "CANDIDATE"]
            "active_role": top_role, # "ADMIN"  — landing hint for the frontend
        }
 
        access_token = Security.create_access_token(
            {
                **token_payload,
                "token_type": "access_token"
            }
        )
        refresh_token = Security.create_refresh_token(
            {
                **token_payload, 
                "token_type": "refresh_token"
            }
        )
 
        return {
            "user_roles": roles,
            "active_role": top_role,
            "user_id": user.user_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
 
    @staticmethod
    def refresh_token(token, db):
        data = Security.decode_token(token)
        access_token = Security.create_access_token(data)
        return {
            "access_token": access_token,
            "refresh_token": token,
        }