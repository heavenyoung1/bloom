from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.models.attorney import AttorneyORM
from backend.core.dependencies import get_async_session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[AttorneyORM, int], None]:
    '''
    Адаптер БД для FastAPI Users.
    '''
    yield SQLAlchemyUserDatabase[AttorneyORM, int](session, AttorneyORM)
