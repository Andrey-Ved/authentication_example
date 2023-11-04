from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core import settings
from app.core.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UserDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(
        password: str
) -> str:

    return pwd_context.hash(
        password
    )


def verify_password(
        plain_password,
        hashed_password,
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
        data: dict
) -> str:

    to_encode = data.copy()
    expire = datetime.utcnow() \
             + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )


async def authenticate_user(
        email: EmailStr,
        password: str
):
    user = await UserDAO.find_one_or_none(
        email=email,
    )

    if not user:
        raise IncorrectEmailOrPasswordException

    if not verify_password(
            password,
            user.hashed_password,
    ):
        raise IncorrectEmailOrPasswordException

    return user


print('init users services')
