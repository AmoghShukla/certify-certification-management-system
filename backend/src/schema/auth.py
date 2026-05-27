from typing import List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from fastapi import File, UploadFile
from src.model.enum import UserTitle
 
 
class Certificate(BaseModel):
    user_certificate: UploadFile = File()
 
 
class RegisterUser(Certificate, BaseModel):
    user_title: UserTitle
    user_first_name: str
    user_last_name: str
    user_email: EmailStr
    user_password: str = Field(..., min_length=8, max_length=12)
    user_confirm_password: str = Field(..., min_length=8, max_length=12)
    user_degree: str
    user_passing_year: int
 
 
class Register(RegisterUser):
    pass
 
 
class LoginUser(BaseModel):
    user_email: EmailStr
    user_password: str = Field(min_length=8, max_length=12)
 
 
class LoginResponse(BaseModel):
    user_roles: List[str]           
    active_role: str  
    user_id: UUID
    access_token: str
    refresh_token: str
    token_type: str = Field(default="Bearer")
 