from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr, Field

from backend.src.model.enum import UserTitle

class Certificate(BaseModel):
    user_certificate : UploadFile = File() 

class RegisterUser(Certificate, BaseModel):
    user_title : UserTitle
    user_first_name : str 
    user_last_name : str 
    user_email : EmailStr 
    user_password : str = Field(...,min_length=8, max_length=12)
    user_confirm_password : str = Field(...,min_length=8, max_length=12)
    user_degree : str 
    user_passing_year : int



class Register(RegisterUser):
    pass

class ProductUploadSchema(BaseModel):
    name: str
    price: float
    description: str | None = None
    profile_image: UploadFile

class LoginUser(BaseModel):
    user_email : EmailStr
    user_password : str = Field(min_length=8, max_length=12)

class LoginResponse(BaseModel):
    user_role : str
    user_id : UUID
    access_token : str
    refresh_token : str
    token_type : str = Field(default="Bearer")
