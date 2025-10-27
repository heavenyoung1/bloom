from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import Settings


class DataBaseConnection:
    '''
    Управление подключением к PostgreSQL с async поддержкой.
    
    Принципы:
    - Все параметры берутся из Settings (single source of truth)
    - Один engine и sessionmaker на приложение
    - Async context manager для безопасной работы с сессией
    '''

    def __init__(self, settings: Settings):
        self.settings = settings
        
        self.engine = create_async_engine(
            settings.url(),
            echo=settings.echo,                     # Логгирование SQL-запросов для отладки
            pool_pre_ping=settings.pool_pre_ping,   # Лечит «мертвые» коннекты (проверять соединение перед использованием (защита от dead connections))
            pool_size=settings.pool_size,           # Тюнинг пула по ситуации (сколько соединений держать в пуле)
            max_overflow=settings.max_overflow,     # Сколько дополнительных можно создать при пиках
        )

        self.AsyncSessionLocal = async_sessionmaker(
            self.engine,                            # Откуда брать соединения
            class_=AsyncSession,                    # Указывает, какой класс сессии использовать, без этого параметра используется обычная Session
            expire_on_commit=False,                 # Контролирует, что происходит с объектами после commit(). SQLAlchemy отслеживает объекты в памяти (Identity Map)
            autoflush=False,                        # Контролирует, когда SQLAlchemy отправляет изменения в БД
        )

        @asynccontextmanager
        async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
            '''
            Async context manager для создания сессии БД.
        
            ⚠️ ВАЖНО: Коммит/откат управляются UnitOfWork, НЕ здесь!
            
            Эта функция ТОЛЬКО:
            - Создаёт async сессию из фабрики
            - Закрывает сессию после использования
            
            UnitOfWork сам решает: коммитить или откатывать.
            
            Использование:
                async with db.get_session() as session:
                    # Передаём сессию в UnitOfWork
                    uow = UnitOfWork(session)
                    with uow:
                        await uow.users.create(...)
            '''


            sesssion = self.AsyncSessionLocal()
            try:
                yield sesssion
            finally:
                await sesssion.close()
