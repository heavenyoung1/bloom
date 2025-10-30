from backend.core.logger import logger
from backend.core.db.uow import AsyncUnitOfWork

from functools import wraps
from typing import Callable, Any


def with_uow(commit: bool = False):
    """
    Декоратор для управления UnitOfWork.

    Args:
        commit (bool):
            - True: сохраняет изменения в БД
            - False: откатывает все изменения (для чтения)

    Использование:
        class UserService:
            def __init__(self, db: Database):
                self.db = db

            @with_uow(commit=False)  # Только читаем
            async def get_user(self, user_id: int):
                return await self.uow.user_repository.get(user_id)

            @with_uow(commit=True)  # Записываем и сохраняем
            async def create_user(self, name: str, email: str):
                return await self.uow.user_repository.create(name, email)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            # 1. Получаем сессию из Database
            async with self.db.get_session() as session:
                # 2. Создаём UnitOfWork с этой сессией
                uow = AsyncUnitOfWork(session)

                # 3. Входим в UOW контекст
                async with uow:
                    # 4. Сохраняем UOW в self для доступа внутри метода
                    self.uow = uow

                    try:
                        # 5. Вызываем оригинальный метод
                        result = await func(self, *args, **kwargs)

                        # 6. Логика управления транзакцией
                        if not commit:
                            # ❌ Откатываем все изменения (для операций чтения)
                            await self.uow.rollback()
                            logger.debug(
                                f'Функция {func.__name__}: изменения откачены (commit=False)'
                            )
                        # Если commit=True, откат произойдёт только при ошибке
                        # Успешный коммит произойдёт в __aexit__

                        return result

                    except Exception as e:
                        logger.error(f'Ошибка в {func.__name__}: {str(e)}')
                        # Откат произойдёт автоматически в __aexit__
                        raise

                    finally:
                        # 7. Очищаем ссылку на UOW
                        self.uow = None

        return wrapper

    return decorator
