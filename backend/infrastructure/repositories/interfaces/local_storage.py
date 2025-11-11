from abc import ABC, abstractmethod
from pathlib import Path
import os


# Интерфейс для работы с файлами (можешь менять реализацию!)
class IFileStorage(ABC):
    '''Абстракция для хранения файлов. Не важно где - на диске или в облаке'''

    @abstractmethod
    async def save_file(self, file_path: str, file_content: bytes) -> str:
        '''Сохранить файл и вернуть путь/ID'''
        pass

    @abstractmethod
    async def get_file(self, file_path: str) -> bytes:
        '''Получить содержимое файла'''
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        '''Удалить файл'''
        pass
