from backend.application.interfaces.repositories.case_repo import ICaseRepository
from backend.application.dto.case import CreateCaseDTO
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class CaseValidator:
    def __init__(self, repo: ICaseRepository):
        self.repo = repo

    async def validate_on_create(self, dto: CreateCaseDTO) -> None:
        '''Валидировать данные при создании дела'''

        #
        client = await self.repo.get(dto.client_id)
        if not client:
            logger(f'Клиент с ID клиента {dto.client_id} не найден')
            raise ValidationException(f'Клиент с ID клиента {dto.client_id} не найден')

        # Клиент должен принадлежать юристу
        if client.owner_attorney_id != dto.attorney_id:
            logger.warning(
                f'Клиент {dto.client_id} не принадлежит юристу {dto.attorney_id}'
            )
            raise ValidationException(f'Клиент не принадлежит юристу {dto.attorney_id}')

        # Юрист должен существовать
        attorney = await self.attorney_repo.get(dto.attorney_id)
        if not attorney:
            logger.warning(f'Юрист {dto.attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {dto.attorney_id} не найден')
