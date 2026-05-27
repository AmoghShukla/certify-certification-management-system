from datetime import datetime, timezone
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from backend.src.model.enum import UserTitle, UserRole

class UserResponse(BaseModel):
    user_id : UUID
    user_title : UserTitle
    user_first_name : str
    user_last_name : str
    user_email : EmailStr
    user_role : UserRole
    user_degree : str
    user_passing_year : int 
    updated_at : datetime = Field(default=datetime.now(timezone.utc))

class GetUser(BaseModel):
    user_id : UUID
    user_title : UserTitle
    user_first_name : str
    user_last_name : str
    user_email : EmailStr
    user_role : UserRole

class GetByRole(BaseModel):
    user_id : UUID
    user_title : UserTitle
    user_first_name : str
    user_last_name : str
    user_email : EmailStr

class GetAllUser(BaseModel):
    user_id : UUID
    user_title : UserTitle
    user_first_name : str
    user_last_name : str
    user_email : EmailStr
    user_role : str
    is_deleted : bool

class CreateAdminMain(BaseModel):
    admin_title : str
    admin_first_name : str
    admin_last_name : str
    admin_email : str
    admin_password : str = Field(min_length=8, max_length=12)
    admin_confirm_password : str = Field(min_length=8, max_length=12)
    
class CreateAdmin(BaseModel):
    admin_title : str
    admin_first_name : str
    admin_last_name : str
    admin_email : str
    admin_password : str = Field(min_length=8, max_length=12)
    admin_confirm_password : str = Field(min_length=8, max_length=12)
    user_certificate : str | None= Field(default="Random_File.png") 
    user_degree : str | None
    user_passing_year : int | None


class UserByMocStatus(BaseModel):
    user_id : UUID
    user_title : UserTitle
    user_first_name : str
    user_last_name : str
    user_email : EmailStr
    user_role : UserRole
    moc_id : UUID
    cycle_id : UUID