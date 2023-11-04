from fastapi import APIRouter, Depends, Response

from app.users.schemas import SUserAuth
from app.users.models import Users
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.services import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.core.exceptions import (
    CannotAddDataToDatabase,
    UserAlreadyExistsException,
)


router = APIRouter()


@router.post("/register", status_code=201)
async def register_user(
        user_data: SUserAuth = Depends()
) -> None:

    existing_user = await UserDAO.find_one_or_none(
        email=user_data.email
    )

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)

    new_user = await UserDAO.add(
        email=user_data.email,
        hashed_password=hashed_password,
    )

    if not new_user:
        raise CannotAddDataToDatabase


@router.post("/login")
async def login_user(
        response: Response,
        user_data: SUserAuth = Depends()
) -> dict[str, str]:

    user = await authenticate_user(
        user_data.email,
        user_data.password,
    )
    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        "example_access_token",
        access_token,
        httponly=True,
    )
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(
        response: Response
) -> None:

    response.delete_cookie(
        "example_access_token",
    )


@router.get("/me")
async def read_users_me(
        current_user: Users = Depends(get_current_user)
) -> str:

    return current_user.email


print('init users routers')
