from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.logger import logger


class AsyncUnitOfWork:
    '''
    Управление транзакцией для async приложения.

    Ключевые моменты:
    - Инициализируется с готовой сессией (не создает сама)
    - Управляет коммит/откат транзакции
    - Все репозитории используют ОДНУ сессию
    '''

    def __init__(self, session: AsyncSession) -> None:
        '''
        Args:
            session: AsyncSession из Database.get_session()
        '''
        self.session = session

        # Инициализируем репозитории с общей сессией
        # (будут созданы в __aenter__)
        self.user_repository = None
        self.product_repository = None
        self.price_repository = None

    async def __aenter__(self):
        '''Вход в async context manager.'''
        # from src.infrastructure.database.repositories import (
        #     UserRepositoryImpl,
        #     ProductRepositoryImpl,
        #     PriceRepositoryImpl,
        # )

        # Инициализируем репозитории с ОДНОЙ сессией
        # self.user_repository = UserRepositoryImpl(self.session)
        # self.product_repository = ProductRepositoryImpl(self.session)
        # self.price_repository = PriceRepositoryImpl(self.session)

        logger.info('🏗️ AsyncUnitOfWork инициализирован')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        '''Выход из async context manager.'''
        try:
            if exc_type is not None:
                # ❌ Была ошибка - откатываем
                logger.warning(f'Исключение в UoW: {exc_type.__name__}: {exc_val}')
                await self.rollback()
            else:
                # ✅ Всё ОК - коммитим
                await self.commit()
        finally:
            # Не закрываем сессию! Database отвечает за это
            logger.info('✅ AsyncUnitOfWork завершил работу')

    async def commit(self) -> None:
        '''Фиксация изменений.'''
        if self.session:
            try:
                await self.session.commit()
                logger.info('✅ Транзакция зафиксирована')
            except Exception as e:
                logger.error(f'❌ Ошибка при коммите: {e}')
                raise

    async def rollback(self) -> None:
        '''Откат изменений.'''
        if self.session:
            try:
                await self.session.rollback()
                logger.info('🔄 Транзакция откачена')
            except Exception as e:
                logger.error(f'❌ КРИТИЧЕСКАЯ ОШИБКА при rollback: {e}')
                raise
