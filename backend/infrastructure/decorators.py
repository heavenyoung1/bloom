from functools import wraps
from typing import Callable, Awaitable, TypeVar, Any
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.core.logger import logger
from backend.core.exceptions import DatabaseErrorException

T = TypeVar('T')


def handle_db_errors(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    '''
    Декоратор для единообразной обработки ошибок SQLAlchemy в репозиториях.

    Ловит:
    - IntegrityError — нарушение уникальности/внешних ключей
    - Все остальные SQLAlchemyError — общие ошибки БД
    '''

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            logger.error(f'Нарушение целостности БД в {func.__name__}: {e.orig}')
            raise DatabaseErrorException(
                'Не удалось выполнить операцию: нарушение уникальности или внешнего ключа.'
            ) from e
        except SQLAlchemyError as e:
            logger.error(f'Ошибка БД в {func.__name__}: {e}')
            raise DatabaseErrorException(
                'Ошибка базы данных. Попробуйте позже или обратитесь к администратору.'
            ) from e

    return wrapper
