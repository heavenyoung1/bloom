"""
Сервис для извлечения метаданных из файлов.
Определяет MIME тип, размер файла и другую полезную информацию.
"""

import mimetypes
from typing import Optional

# Опциональная библиотека для более точного определения MIME типа
try:
    import magic

    MAGIC_AVAILABLE = True
except (ImportError, OSError):
    # OSError может возникнуть, если libmagic не установлен в системе
    MAGIC_AVAILABLE = False


class FileMetadataExtractor:
    '''Сервис для извлечения метаданных из файлов'''

    @staticmethod
    def get_mime_type(file_content: bytes, file_name: str) -> str:
        '''
        Определяет MIME тип файла.

        Args:
            file_content: Содержимое файла в байтах
            file_name: Имя файла (для определения по расширению)

        Returns:
            MIME тип файла (например, 'application/pdf', 'image/jpeg')
        '''
        # Сначала пробуем определить по содержимому (более точно)
        if MAGIC_AVAILABLE:
            try:
                mime_type = magic.from_buffer(file_content, mime=True)
                if mime_type:
                    return mime_type
            except Exception:
                # Если magic не доступен, используем mimetypes
                pass

        # Fallback: определяем по расширению файла
        mime_type, _ = mimetypes.guess_type(file_name)
        return mime_type or 'application/octet-stream'

    @staticmethod
    def get_file_size(file_content: bytes) -> str:
        '''
        Возвращает размер файла в байтах как строку.

        Args:
            file_content: Содержимое файла в байтах

        Returns:
            Размер файла в байтах (строка)
        '''
        return str(len(file_content))

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        '''
        Форматирует размер файла в человекочитаемый вид.

        Args:
            size_bytes: Размер файла в байтах

        Returns:
            Форматированный размер (например, "1.5 MB")
        '''
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f'{size_bytes:.2f} {unit}'
            size_bytes /= 1024.0
        return f'{size_bytes:.2f} TB'

    @staticmethod
    def extract_all_metadata(file_content: bytes, file_name: str) -> dict[str, str]:
        '''
        Извлекает все метаданные файла.

        Args:
            file_content: Содержимое файла в байтах
            file_name: Имя файла

        Returns:
            Словарь с метаданными: mime_type, file_size
        '''
        return {
            'mime_type': FileMetadataExtractor.get_mime_type(file_content, file_name),
            'file_size': FileMetadataExtractor.get_file_size(file_content),
        }
