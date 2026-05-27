import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.src.utils.logger import get_logger

import re
from backend.src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
logger = get_logger(__name__)   

def get_current_user(token: str =  Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if not payload:
            raise jwt.exceptions.InvalidTokenError("Invalid Token!!!")

        user_id = payload.get('sub')
        user_role = payload.get('user_role')

        if not user_id or not user_role:
            raise jwt.exceptions.InvalidTokenError("Invalid Token!!!")
        
        logger.info("Fetched Current User!!")
        return {
            'user_id': user_id,
            'user_role': user_role
        }

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        ) from e



def required_role(roles: list):
    allowed_roles = {
        role.value.upper() if hasattr(role, "value") else str(role).upper()
        for role in roles
    }

    def role_checker(user=Depends(get_current_user)):
        if str(user['user_role']).upper() not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not Authorised!!",
            )
        return user

    return role_checker


def normalize_search(text : str) -> str:
    text = text.lower().strip()

    text = re.sub(r"\s+", " ", text)
    return text