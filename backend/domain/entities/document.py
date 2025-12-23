from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    id: Optional[int]
    file_name: str
    storage_path: str
    file_size: str
    case_id: int
    attorney_id: int
    description: str
    mime_type: Optional[str] = None

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        file_name: str,
        storage_path: str,
        file_size: str,
        case_id: int,
        attorney_id: int,
        description: str = '',
        mime_type: Optional[str] = None,
    ) -> 'Document':
        '''Фабричный метод для создания нового документа.'''
        return Document(
            id=None,  # ID будет присвоен после сохранения в базе данных
            file_name=file_name,
            storage_path=storage_path,
            file_size=file_size,
            case_id=case_id,
            attorney_id=attorney_id,
            description=description,
            mime_type=mime_type,
        )
