import asyncio

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core import settings
from app.users.router import router as router_auth
from app.core.db_services import db_init, db_clear
from app.core.db_base import Base, async_engine


@asynccontextmanager
async def lifespan(application: FastAPI):
    print('start app')

    yield

    if settings.DB_CLEAR_AT_THE_END:
        await db_clear(async_engine, Base)

    print('stop app')


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(
    router_auth,
    prefix="/auth",
    tags=["Auth"],
)


def main():

    asyncio.run(
        db_init(async_engine, Base)
    )

    print(
        f'\n'
        f'INFO:     Documentation is available at -'
        f' http://127.0.0.1:{settings.API_PORT}/docs'
        f'\n'
    )

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=settings.API_PORT
    )


if __name__ == '__main__':
    main()
