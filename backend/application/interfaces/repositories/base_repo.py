# backend/infrastructure/repositories/interfaces/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

T = TypeVar('T')  # Тип доменной сущности


class IBaseRepository(Generic[T], ABC):
    '''
    Базовый интерфейс для всех репозиториев.
    Определяет стандартные CRUD-операции.
    '''

    @abstractmethod
    async def save(self, entity: T) -> T:
        '''Сохраняет сущность и возвращает её с обновлённым ID.'''
        ...

    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        '''Получить сущность по ID. Возвращает None, если не найдена.'''
        ...

    @abstractmethod
    async def update(self, entity: T) -> T:
        '''Обновляет сущность. Должен содержать ID.'''
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        '''Удаляет сущность по ID. Возвращает True при успехе.'''
        ...
