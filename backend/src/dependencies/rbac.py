import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from src.utils.logger import get_logger
 
import re
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
logger = get_logger(__name__)
 
 
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
 
        user_id = payload.get("sub")
        roles = payload.get("user_roles")         
        active_role = payload.get("active_role")
 
        if not user_id or not roles:
            raise jwt.exceptions.InvalidTokenError("Invalid token payload")
 
        logger.info("Fetched current user — roles: %s", roles)
        return {
            "user_id": user_id,
            "roles": roles,                   # list e.g. ["ADMIN", "CANDIDATE"]
            "active_role": active_role,       # highest-privilege role
        }
 
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e
 
 
def required_role(roles: list):
    allowed_roles = {
        role.value.upper() if hasattr(role, "value") else str(role).upper()
        for role in roles
    } 
    def role_checker(user=Depends(get_current_user)):
        user_roles = {r.upper() for r in user["user_roles"]}
        if not user_roles.intersection(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorised",
            )
        return user
    return role_checker
 
 
def normalize_search(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())