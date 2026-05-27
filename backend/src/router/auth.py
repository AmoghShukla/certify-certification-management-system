from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Form, UploadFile, File
from pydantic import EmailStr
from sqlalchemy.orm import Session

from backend.src.model.enum import UserRole, UserTitle
from backend.src.database.Session import get_db
from backend.src.schema.auth import LoginResponse, LoginUser, Register, RegisterUser
from backend.src.schema.user import UserResponse
from backend.src.service.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register')
def user_register(
    background_tasks : BackgroundTasks,
    user_title: Annotated[UserTitle, Form()],
    user_first_name: Annotated[str, Form()],
    user_last_name: Annotated[str, Form()],
    user_email: Annotated[EmailStr, Form()],
    user_password: Annotated[str, Form()],
    user_confirm_password: Annotated[str, Form()],
    user_degree : Annotated[str, Form()],
    user_passing_year : Annotated[int, Form()],
    user_certificate: UploadFile = File(...),
    db : Session = Depends(get_db)
    ):
    payload = RegisterUser(
        user_title=user_title,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        user_email=user_email,
        user_password=user_password,
        user_confirm_password=user_confirm_password,
        user_certificate=user_certificate,
        user_degree=user_degree,
        user_passing_year=user_passing_year
    )
    return AuthService.register_user(payload, background_tasks, db)

@router.post('/login', response_model=LoginResponse)
def user_login(user_details: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    return AuthService.login_user(user_details, db)

@router.post('/refresh_token')
def refresh_token(refresh_token, db : Session = Depends(get_db)):
    return AuthService.refresh_token(refresh_token, db)