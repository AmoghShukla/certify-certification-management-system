from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy import select

from backend.src.model import UserClass, UserRoleClass
from backend.src.model.enum import UserRole
from backend.src.repository import AuthRepository, UserRoleRepository, UserRepository, MocRepository
from backend.src.core.security import Security
from backend.src.exceptions import CustomException
from backend.src.utils.centralized import Centralized

from sqlalchemy.orm import Session


class UserService:

    # @staticmethod
    # def update_user(user_email_id, updated_payload, db : Session):
    #     user = UserRepository.get_user_by_email_id(user_email_id, db)

    #     if not user:
    #         raise CustomException.UserNotFoundError()
        
    #     new_user_payload = updated_payload.model_dump()

    @staticmethod
    def get_user_by_email_id(user_email_id, db : Session):
        user =  UserRepository.get_user_by_email_id(user_email_id, db)
        role = UserRoleRepository.get_user_role_by_user_id(user.user_id, db)

        if not user:
            raise CustomException.UserNotFoundError()
        
        return {
                'user_id' : user.user_id,
                'user_title' : user.user_title,
                'user_first_name' : user.user_first_name,
                'user_last_name' : user.user_last_name,
                'user_email' : user.user_email,
                'user_role' : role.user_role
        }

    @staticmethod
    def create_admin(payload, db):
        user = UserRepository.get_user_by_email_id(payload.admin_email, db)
        if user:
            raise CustomException.UserAlreadyExists()
        if payload.admin_password != payload.admin_confirm_password:
            raise CustomException.PasswordDoesNotMatch()
        password = Security.hash_password(payload.admin_password)
        new_payload = UserClass(
            user_title = payload.admin_title,
            user_first_name = payload.admin_first_name,
            user_last_name = payload.admin_last_name,
            user_email = payload.admin_email,
            user_password = password,
            user_certificate = None, 
            user_degree = None,
            user_passing_year = None 
        )
        Created_user =  AuthRepository.register_user(new_payload, db)
        
        role_payload = UserRoleClass(
            user_id = Created_user.user_id,
            user_role = UserRole.ADMIN,
            updated_at = datetime.now(timezone.utc)
        )
        Created_role = UserRoleRepository.register_role(role_payload, db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f"Admin created successfully."
        )
    
    @staticmethod
    def get_user_by_role(role, db):

        query = select(UserRoleClass)
        model = UserRoleClass
        filters = {'user_role' : role.upper()}
        
        final_query = Centralized.apply_filters(query, model, filters)
        admin_role = UserRoleRepository.get_user_by_role(final_query, db)
        
        if not admin_role:
            raise CustomException.UserRoleNotFoundError()

        output = []

        for role in admin_role:
            user = UserRepository.get_user_by_user_id(role.user_id, db)
            output.append(user)
        return output
    
    @staticmethod
    def get_all_user(page_no, db):
        all_users = UserRepository.get_all_user(page_no, db)

        output = []
        for user in all_users:
            all_user_role = UserRoleRepository.get_user_role_by_user_id(user.user_id, db)
            output.append({
                'user_id' : user.user_id,
                'user_title' : user.user_title,
                'user_first_name' : user.user_first_name,
                'user_last_name' : user.user_last_name,
                'user_email' : user.user_email,
                'user_role' : all_user_role.user_role,
                'is_deleted' : user.is_deleted
            })
        return output
            
    @staticmethod
    def get_users_with_moc_status(moc_status, page_no, db):
        all_moc = MocRepository.get_users_by_moc_status(moc_status, page_no, db)

        if not all_moc:
            raise CustomException.NotFoundError('MOC')

        return [
            {
                'user_id': moc['user_id'],
                'user_title': moc['user_title'],
                'user_first_name': moc['user_first_name'],
                'user_last_name': moc['user_last_name'],
                'user_email': moc['user_email'],
                'user_role': moc['user_role'],
                'moc_id': moc['moc_id'],
                'cycle_id': moc['cycle_id'],
            }
            for moc in all_moc
        ]


