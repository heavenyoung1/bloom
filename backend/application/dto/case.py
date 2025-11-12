from backend.infrastructure.models.case import CaseStatus

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from typing import Optional
from datetime import datetime


class CreateCaseDTO(BaseModel):
    '''DTO для создания нового дела'''

    name: str = Field(..., max_length=255, description='Название дела')
    client_id: int = Field(
        ...,
        gt=0,
        description='ID клиента, прикрепленного к делу',
    )
    attorney_id: int = Field(
        ...,
        gt=0,
        description='ID юриста, ответственного за клиента',
    )
    status: CaseStatus = Field(
        ...,
        description=(
            'Статус дела. Возможные значения:\n'
            ' - Новое: дело создано, но не принято в работу\n'
            ' - В работе: юрист ведёт дело\n'
            ' - На паузе: временная приостановка\n'
            ' - Завершено: успешно завершено\n'
            ' - Закрыто: закрыто без результата\n'
            ' - Отменено: отменено до начала работы\n'
            ' - Архивировано: перемещено в архив'
        ),
    )
    description: str = Field(
        ...,
        max_length=255,  # увеличено для развёрнутого описания
        description=(
            'Подробное описание сути дела: ключевые вопросы, требования, '
            'участники, правовые основания'
        ),
    )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'Споры по недвижимости',
                'client_id': 1,
                'attorney_id': 1,
                'status': 'Новое',
                'description': 'Разрешение спора о праве собственности на квартиру',
            }
        }
    )


class UpdateCaseDTO(BaseModel):
    '''DTO для частичного обновления дела (PATCH)'''

    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description='Название дела',
    )
    status: Optional[str] = Field(
        ...,
        default=None,
        description=(
            'Статус дела. Возможные значения:\n'
            ' - Новое: дело создано, но не принято в работу\n'
            ' - В работе: юрист ведёт дело\n'
            ' - На паузе: временная приостановка\n'
            ' - Завершено: успешно завершено\n'
            ' - Закрыто: закрыто без результата\n'
            ' - Отменено: отменено до начала работы\n'
            ' - Архивировано: перемещено в архив'
        ),
    )
    description: Optional[str] = Field(
        ...,
        default=None,
        max_length=255,  # увеличено для развёрнутого описания
        description=(
            'Подробное описание сути дела: ключевые вопросы, требования, '
            'участники, правовые основания'
        ),
    )


class UpdateCaseStatusDTO(BaseModel):
    '''DTO для частичного обновления дела (PATCH)'''

    status: CaseStatus = Field(
        ...,
        description=(
            'Статус дела. Возможные значения:\n'
            ' - Новое: дело создано, но не принято в работу\n'
            ' - В работе: юрист ведёт дело\n'
            ' - На паузе: временная приостановка\n'
            ' - Завершено: успешно завершено\n'
            ' - Закрыто: закрыто без результата\n'
            ' - Отменено: отменено до начала работы\n'
            ' - Архивировано: перемещено в архив'
        ),
    )


class CaseResponseDTO(BaseModel):
    '''DTO для ответа: полная информация о деле'''

    id: int
    name: str
    client_id: int
    attorney_id: int
    status: CaseStatus
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseListItemDTO(BaseModel):
    '''DTO для списка дел'''

    id: int
    name: str
    client_id: int
    attorney_id: int
    status: CaseStatus

    class Config:
        from_attributes = True
