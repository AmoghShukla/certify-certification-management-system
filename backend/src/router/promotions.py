from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from backend.src.service.promotions import PromotionsService
from backend.src.database.Session import get_db
from backend.src.schema.auth import LoginResponse, LoginUser, RegisterUser
from backend.src.schema.user import UserResponse
from backend.src.service.auth import AuthService


router = APIRouter(prefix='/promotions', tags=['Promotions'])

@router.post('/register', response_model=UserResponse)
def make_admin(email_id : EmailStr, db : Session = Depends(get_db)):
    return PromotionsService.promote_to_admin(email_id, db)
