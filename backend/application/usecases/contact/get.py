from backend.application.dto.contact import ContactResponse
from backend.domain.entities.contact import Contact
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import GetContactByIdQuery
from backend.application.policy.case_policy import CasePolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class GetCaseByIdUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        '''Получение клиента по ID'''
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetContactByIdQuery,
    ) -> 'ContactResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело
                contact = await uow.contact_repo.get(cmd.contact_id)

                if not contact:
                    logger.error(f'Дело с ID {cmd.case_id} не найдено.')
                    raise EntityNotFoundException(f'Дело не найдено.')

                logger.info(f'Дело получено: ID = {cmd.case_id}')
                return ContactResponse.model_validate(contact)
            except Exception as e:
                logger.error(f'Ошибка при получении дела: {e}')
                raise e
