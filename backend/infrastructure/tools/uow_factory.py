from backend.core.db.database import DataBaseConnection
from backend.infrastructure.tools.uow import AsyncUnitOfWork
from backend.core.logger import logger
from typing import AsyncGenerator
from contextlib import asynccontextmanager


class UnitOfWorkFactory:
    '''Фабрика для создания UnitOfWork через DataBaseConnection.'''

    def __init__(self, db: DataBaseConnection):
        self.db = db
        logger.info('✅ UnitOfWorkFactory инициализирована')

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[AsyncUnitOfWork, None]:
        '''
        Создаёт UnitOfWork с управлением сессией.

        Использование:
            async with factory.create() as uow:
                await uow.attorney_repo.get(1)
        '''
        async with self.db.get_session() as session:
            uow = AsyncUnitOfWork(session)
            async with uow:
                yield uow

    async def close(self) -> None:
        '''Закрытие соединений с БД при завершении приложения.'''
        await self.db.dispose()
        logger.info('DataBaseConnection закрыта')
