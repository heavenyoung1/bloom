from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateDocumentCommand:
    '''Команда для создания нового документа'''

    file_name: str
    storage_path: str
    file_size: str
    case_id: int
    attorney_id: int
    description: str = ''
    mime_type: Optional[str] = None


@dataclass
class DeleteDocumentCommand:
    '''Команда для удаления документа'''

    document_id: int
    attorney_id: int  # для проверки прав доступа


@dataclass
class GetDocumentByIdQuery:
    '''Запрос для получения документа по ID'''

    document_id: int
    attorney_id: int  # для проверки прав доступа


@dataclass
class GetDocumentsForCaseQuery:
    '''Запрос для получения всех документов дела'''

    case_id: int
    attorney_id: int  # для проверки прав доступа

