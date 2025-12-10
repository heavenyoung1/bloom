from backend.application.interfaces.repositories.contact_repo import IContactRepository
from backend.application.interfaces.repositories.case_repo import ICaseRepository

from backend.application.dto.contact import CreateContactDTO
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class ContactValidator:
    '''Валидатор для контактов'''

    def __init__(
        self,
        contact_repo: IContactRepository,
        case_repo: ICaseRepository,
    ):
        self.contact_repo = contact_repo
        self.case_repo = case_repo

    async def validate_on_create(self, dto: CreateContactDTO) -> None:
        '''Валидировать данные при создании контакта'''

        # Дело должно существовать
        case = await self.case_repo.get(dto.case_id)
        if not case:
            logger.warning(f'Дело {dto.case_id} не найдено')
            raise EntityNotFoundException(f'Дело с ID {dto.case_id} не найдено')
