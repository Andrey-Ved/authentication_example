from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.core import settings
from app.users.dao import UserDAO
from app.users.models import Users
from app.core.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)


def get_token(
        request: Request
) -> str:

    token = request.cookies.get("example_access_token")

    if not token:
        raise TokenAbsentException

    return token


async def get_current_user(
        token: str = Depends(get_token)
) -> Users:

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_one_or_none(id=int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user


print('init users dependencies')
