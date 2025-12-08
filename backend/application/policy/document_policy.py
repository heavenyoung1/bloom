from backend.infrastructure.repositories.interfaces.document_repo import (
    IDocumentRepository,
)
from backend.infrastructure.repositories.interfaces.case_repo import (
    ICaseRepository,
)
from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)

#!!!!!!!!!!!!!!!
from backend.application.dto.document import CreateDocumentDTO
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class DocumentValidator:
    '''Валидатор для документов'''

    def __init__(
        self,
        document_repo: IDocumentRepository,
        case_repo: ICaseRepository,
        attorney_repo: IAttorneyRepository,
    ):
        self.document_repo = document_repo
        self.case_repo = case_repo
        self.attorney_repo = attorney_repo

    async def validate_on_create(self, dto: CreateDocumentDTO) -> None:
        '''Валидировать данные при создании документа'''

        # Дело должно существовать (если указано)
        if dto.case_id:
            case = await self.case_repo.get(dto.case_id)
            if not case:
                logger.warning(f'Дело {dto.case_id} не найдено')
                raise EntityNotFoundException(f'Дело с ID {dto.case_id} не найдено')

        # Юрист должен существовать (если указан)
        if dto.attorney_id:
            attorney = await self.attorney_repo.get(dto.attorney_id)
            if not attorney:
                logger.warning(f'Юрист {dto.attorney_id} не найден')
                raise EntityNotFoundException(f'Юрист с ID {dto.attorney_id} не найден')
