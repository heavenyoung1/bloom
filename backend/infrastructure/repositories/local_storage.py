from backend.infrastructure.repositories.interfaces import IFileStorage
import os


class LocalFileStorage(IFileStorage):
    '''Хранилище в файловой системе Linux'''

    def __init__(self, base_path: str = '/opt/CRM/storage/'):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file_path: str, file_content: bytes) -> str:
        '''Сохраняет файл на диск'''
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'wb') as f:
            f.write(file_content)

        return str(file_path)  # Возвращаем относительный путь для БД

    async def delete_file(self, file_path: str) -> bool:
        '''Удаляет файл с диска'''
        full_path = self.base_path / file_path
        if full_path.exists():
            os.remove(full_path)
            return True
        return False

    async def get_file(self, file_path: str) -> bytes:
        '''Читает файл с диска'''
        full_path = self.base_path / file_path
        with open(full_path, 'rb') as f:
            return f.read()
