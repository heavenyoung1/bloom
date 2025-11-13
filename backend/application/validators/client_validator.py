from backend.infrastructure.repositories.interfaces.client_repo import (
    IClientRepository,
)
from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.dto.client import CreateClientDTO
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger

class ClientValidator:
    '''Валидатор для клиентов'''
    
    def __init__(
        self,
        client_repo: IClientRepository,
        attorney_repo: IAttorneyRepository,
    ):
        self.client_repo = client_repo
        self.attorney_repo = attorney_repo

    async def validate_on_create(self, dto: CreateClientDTO) -> None:
        '''Валидировать данные при создании клиента'''
        
        # Юрист должен существовать
        attorney = await self.attorney_repo.get(dto.owner_attorney_id)
        if not attorney:
            logger.warning(f'Юрист {dto.owner_attorney_id} не найден')
            raise EntityNotFoundException(
                f'Юрист с ID {dto.owner_attorney_id} не найден'
            )
        
        # Email должен быть уникален (если указан)
        if dto.email:
            existing = await self.client_repo.get_by_email(dto.email)
            if existing and existing.owner_attorney_id == dto.owner_attorney_id:
                logger.warning(f'Email {dto.email} уже используется этим юристом')
                raise ValidationException(
                    f'Email {dto.email} уже используется этим юристом'
                )
        
        # Номер телефона должен быть уникален (если указан)
        if dto.phone:
            existing = await self.client_repo.get_by_phone(dto.phone)
            if existing and existing.owner_attorney_id == dto.owner_attorney_id:
                logger.warning(f'Номер телефона {dto.phone} уже используется')
                raise ValidationException(
                    f'Номер телефона {dto.phone} уже используется'
                )