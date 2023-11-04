from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete, insert, select

from app.core import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    url=settings.DSN,
    # echo=True,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()

        except (SQLAlchemyError, Exception) as e:
            msg = "Cannot insert data into table"

            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: " + msg
            elif isinstance(e, Exception):
                msg = "Unknown Exc: " + msg

            print(msg)
            return None

    @classmethod
    async def delete(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()


print('init db base')
