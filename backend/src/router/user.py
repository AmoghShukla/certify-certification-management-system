from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from backend.src.dependencies.rbac import required_role
from backend.src.model.enum import MocStatus
from backend.src.schema.user import CreateAdminMain, GetAllUser, GetByRole, GetUser, UserByMocStatus
from backend.src.database.Session import get_db
from backend.src.service.user import UserService


router = APIRouter(prefix='/user', tags=['User'])

@router.post('/create_admin')
def create_admin(payload : CreateAdminMain, db : Session = Depends(get_db), user = Depends(required_role(['SUPERADMIN']))):
    return UserService.create_admin(payload, db)

@router.get('/get_user_by_email_id', response_model=GetUser)
def get_user_by_email_id(email_id : EmailStr, db : Session = Depends(get_db)):
    return UserService.get_user_by_email_id(email_id, db)

@router.get('/get_admin', response_model=list[GetByRole])
def get_admin(db : Session = Depends(get_db)):
    return UserService.get_user_by_role("ADMIN",db)

@router.get('/get_candidate', response_model=list[GetByRole])
def get_candidate(db : Session = Depends(get_db)):
    return UserService.get_user_by_role("CANDIDATE",db)

@router.get('/get_diplomate', response_model=list[GetByRole])
def get_diplomate(db : Session = Depends(get_db)):
    return UserService.get_user_by_role("DIPLOMATE",db)

@router.get('/get_user', response_model=list[GetByRole])
def get_user(db : Session = Depends(get_db)):
    return UserService.get_user_by_role("USER",db)

@router.get('/get_all_user', response_model=list[GetAllUser])
def get_all_user(page_no : int, db : Session = Depends(get_db)):
    return UserService.get_all_user(page_no, db)

@router.get('/get_users_with_moc_status', response_model=list[UserByMocStatus])
def get_users_with_moc_status(moc_status : MocStatus, page_no : int, db : Session = Depends(get_db)):
    return UserService.get_users_with_moc_status(moc_status, page_no, db)

