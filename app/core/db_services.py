from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from typing import Type


async def db_init(
        async_engine:  AsyncEngine,
        base: Type[DeclarativeBase]
) -> None:

    async with async_engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

        for table in base.metadata.sorted_tables:
            print(f'init table - {table}')

    print('init db')


async def db_clear(
        async_engine:  AsyncEngine,
        base: Type[DeclarativeBase]
) -> None:

    async with async_engine.begin() as conn:
        await conn.run_sync(base.metadata.reflect)

        for table in base.metadata.sorted_tables:
            await conn.execute(table.delete())

            print(f'db clear - {table}')


print('init db services')
