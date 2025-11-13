from datetime import datetime

from backend.infrastructure.repositories.interfaces.event_repo import (
    IEventRepository,
)
from backend.infrastructure.repositories.interfaces.case_repo import (
    ICaseRepository,
)
from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)

from backend.application.dto.event import CreateEventDTO
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class EventValidator:
    '''Валидатор для событий'''
    
    def __init__(
        self,
        event_repo: IEventRepository,
        case_repo: ICaseRepository,
        attorney_repo: IAttorneyRepository,
    ):
        self.event_repo = event_repo
        self.case_repo = case_repo
        self.attorney_repo = attorney_repo

    async def validate_on_create(self, dto: CreateEventDTO) -> None:
        '''Валидировать данные при создании события'''
        
        # Дело должно существовать
        case = await self.case_repo.get(dto.case_id)
        if not case:
            logger.warning(f'Дело {dto.case_id} не найдено')
            raise EntityNotFoundException(f'Дело с ID {dto.case_id} не найдено')
        
        # Юрист должен существовать
        attorney = await self.attorney_repo.get(dto.attorney_id)
        if not attorney:
            logger.warning(f'Юрист {dto.attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {dto.attorney_id} не найден')
        
        # Дата события не должна быть в прошлом (опционально)
        if dto.event_date < datetime.now(dto.event_date.tzinfo):
            logger.warning(f'Дата события {dto.event_date} в прошлом')
            raise ValidationException('Дата события не может быть в прошлом')