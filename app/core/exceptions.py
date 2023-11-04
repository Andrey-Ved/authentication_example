from fastapi import HTTPException, status


class ExampleException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )


class UserAlreadyExistsException(ExampleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(ExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class TokenExpiredException(ExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has expired"


class TokenAbsentException(ExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is missing"


class IncorrectTokenFormatException(ExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(ExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not present"


class CannotAddDataToDatabase(ExampleException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot add data"


print('init exception')
