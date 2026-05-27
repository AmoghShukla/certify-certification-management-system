from fastapi.responses import JSONResponse
from fastapi import status

class AppException(Exception):

    def __init__(
            self, message, status_code : int = 400
    ):
        self.message = message
        self.status_code = status_code

class AlreadyExistsError(AppException):
    
    def __init__(self, msg):
        super().__init__(
            message=f"{msg} Already Exists",
            status_code=status.HTTP_409_CONFLICT
        )


class UserNotFoundError(AppException):
    
    def __init__(self, msg):
        super().__init__(
            message=f"{msg} Not Found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class NotFoundError(AppException):
    
    def __init__(self, msg):
        super().__init__(
            message=f"{msg} Not Found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class BadRequestError(AppException):

    def __init__(self, message):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class UserRoleNotFoundError(AppException):
    
    def __init__(self):
        super().__init__(
            message="No User with this Role Exist",
            status_code=status.HTTP_404_NOT_FOUND
        )

class UserAlreadyExists(AppException):
    
    def __init__(self):
        super().__init__(
            message="User Already Exists!!!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class PasswordDoesNotMatch(AppException):
    
    def __init__(self):
        super().__init__(
            message="Password Does Not Match!!!",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class PasswordDoesNotMatchError(AppException):
    
    def __init__(self):
        super().__init__(
            message="Password Entered is incorrect",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class RepositoryError(Exception):
    pass

class ServiceError(Exception):
    pass