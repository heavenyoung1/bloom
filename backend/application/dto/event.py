from backend.domain.entities.auxiliary import EventType
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

# Первый аргумент в Field (...) - эллипсис - что поле обязательно
# Если данные не заполнены, будет ошибка валидации.


class EventCreateRequest(BaseModel):
    '''DTO для создания события'''

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    event_type: EventType
    event_date: datetime
    case_id: int
    attorney_id: int

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'Заседание суда',
                'description': 'Рассмотрение дела по существу',
                'event_type': 'court_hearing',
                'event_date': '2024-12-15T10:00:00Z',
                'case_id': 1,
                'attorney_id': 1,
            }
        }


class EventUpdateRequest(BaseModel):
    '''DTO для обновления события'''

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    event_type: Optional[EventType] = None
    event_date: Optional[datetime] = None


class EventResponse(BaseModel):
    '''DTO для ответа: полная информация о событии'''

    id: int
    name: str
    description: Optional[str]
    event_type: EventType
    event_date: datetime
    case_id: int
    attorney_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventListGetRequest(BaseModel):
    '''DTO для списка событий'''

    id: int
    name: str
    event_type: EventType
    event_date: datetime
    case_id: int

    model_config = ConfigDict(from_attributes=True)
