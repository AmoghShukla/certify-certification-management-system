from datetime import datetime, UTC, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from ..exceptions import CustomException

from backend.src.core.config import settings

PasswordContext : PasswordHash = PasswordHash.recommended()

class Security:

    @staticmethod
    def hash_password(password : str):
        try:
            return PasswordContext.hash(password)
        except jwt.PyJWKError as e:
            raise CustomException.ServiceError("Error While Hashing the Password")
        
    @staticmethod
    def verify_password(plain_password, hashed_password):
        try:
            return PasswordContext.verify(plain_password, hashed_password)
        except jwt.PyJWKError as e:
            raise CustomException.ServiceError("Error While Verifying the Password")
        
    @staticmethod
    def create_access_token(data : dict):
        try:
            data_to_encode = data.copy()
            expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

            data_to_encode.update({'exp' : expiry})
            return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except jwt.PyJWKError as e:
            raise CustomException.ServiceError("Error While Creating the Access Token!!")

    @staticmethod
    def create_refresh_token(data : dict):
        try:
            data_to_encode = data.copy()
            expiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

            data_to_encode.update({'exp' : expiry})
            return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except jwt.PyJWKError as e:
            raise CustomException.ServiceError("Error While Creating the Refresh Token!!")

    @staticmethod
    def decode_token(token):
        new_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not new_token:
            raise CustomException.BadRequestError("Error while decoding the token")
        return new_token