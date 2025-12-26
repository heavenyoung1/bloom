from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class DocumentCreateRequest(BaseModel):
    '''DTO для создания нового документа (через загрузку файла)'''

    case_id: int = Field(
        ..., gt=0, description='ID дела, к которому прикрепляется документ'
    )
    description: Optional[str] = Field(
        None, max_length=500, description='Описание документа'
    )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'case_id': 1,
                'description': 'Договор аренды от 01.01.2024',
            }
        }
    )


class DocumentResponse(BaseModel):
    '''DTO для ответа с данными документа'''

    id: int = Field(..., description='ID документа')
    file_name: str = Field(..., description='Имя файла')
    storage_path: str = Field(..., description='Путь к файлу в хранилище')
    file_size: Optional[str] = Field(None, description='Размер файла в байтах')
    case_id: int = Field(..., description='ID дела')
    attorney_id: int = Field(..., description='ID юриста')
    description: str = Field(..., description='Описание документа')
    mime_type: Optional[str] = Field(None, description='MIME тип файла')
    created_at: Optional[datetime] = Field(None, description='Дата создания')
    updated_at: Optional[datetime] = Field(None, description='Дата обновления')

    model_config = ConfigDict(from_attributes=True)


class DocumentListResponse(BaseModel):
    '''DTO для списка документов'''

    documents: list[DocumentResponse] = Field(..., description='Список документов')
    total: int = Field(..., description='Общее количество документов')

    model_config = ConfigDict(from_attributes=True)


# Для внутреннего использования (старое DTO)
class CreateDocumentDTO(BaseModel):
    '''Внутренний DTO для создания документа (используется в валидаторах)'''

    file_name: str
    storage_path: str
    file_size: Optional[str] = None
    case_id: int
    description: str = ''
    mime_type: Optional[str] = None
