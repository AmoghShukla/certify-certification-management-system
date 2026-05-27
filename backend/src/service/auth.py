from datetime import datetime, timezone
import os

from backend.src.model.user_role import UserRoleClass
from backend.src.model.enum import UserRole
from backend.src.repository.auth import AuthRepository
from backend.src.repository.user_role import UserRoleRepository, UserRoleRepository
from backend.src.exceptions import CustomException
from backend.src.repository.user import UserRepository
from backend.src.schema import UserResponse
from backend.src.core.security import Security
from backend.src.service.aws_s3_service import S3Service
from backend.src.service.email_service import send_email
from backend.src.router.user import get_admin

from sqlalchemy.orm import Session

from backend.src.service.user import UserService


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
                    raise CustomException.ServiceError("Error while uploading user certificate!!!")
                payload.user_certificate = uploaded_certificate

            if not os.path.exists('src/utils/temps'):
                os.makedirs('src/utils/temps', exist_ok=True)
            created_user = AuthRepository.register_user(payload, db)
            if not created_user:
                raise CustomException.BadRequestError()
                
            role_payload = UserRoleClass(
                user_id=created_user.user_id,
                user_role=UserRole.USER,
                updated_at=datetime.now(timezone.utc)
            )
            created_role = UserRoleRepository.register_role(role_payload, db)

            admins = UserService.get_user_by_role("ADMIN",db)
            admin_emails = [admin.user_email for admin in admins]
            
            background_tasks.add_task(
                send_email, 
                admin_emails, 
                "User Registration Mail", 
                f"{payload.user_first_name} has been onboarded onto our application"
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
                updated_at=created_user.updated_at
            )
        except CustomException.RepositoryError as e:
            raise CustomException.ServiceError(str(e))

    

    def login_user(payload, db):
        user_email = payload.username
        user_password = payload.password
        user = UserRepository.get_user_by_email_id(user_email, db)
        if not user:
            raise CustomException.UserNotFoundError("User Does Not Exists, Please Register First!!!")

        if not Security.verify_password(user_password, user.user_password):
            raise CustomException.PasswordDoesNotMatchError()
        
        second_user = UserRoleRepository.get_user_role_by_user_id_single(user.user_id, db)
        access_token = Security.create_access_token({
            'sub' : str(user.user_id),
            'user_role' : second_user.user_role.value,
            'token_type' : 'access_token'
        })

        refresh_token = Security.create_refresh_token({
            'sub' : str(user.user_id),
            'user_role' : second_user.user_role.value,
            'token_type' : 'refresh_token'
        })

        return {
            'user_role' : second_user.user_role.value,
            'user_id' : user.user_id,
            'access_token' : access_token,
            'refresh_token' : refresh_token,
            'token_type' : 'Bearer'
        }
        
    @staticmethod
    def refresh_token(token, db):
        data = Security.decode_token(token)

        access_token = Security.create_access_token(data)

        return {
            'accesss_token' : access_token,
            'refresh_token' : token
        }
        






