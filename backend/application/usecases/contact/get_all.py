from backend.application.dto.contact import ContactResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.contact import GetContactsForAttorneyQuery
from typing import List
from backend.core.logger import logger


class GetAllContactsUseCase:
    '''Сценарий: юрист получает все свои контакты'''
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetContactsForAttorneyQuery,
    ) -> List['ContactResponse']:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить все контакты юриста
                contacts = await uow.contact_repo.get_all_for_attorney(cmd.attorney_id)

                # Проверка, что контакты существуют
                if not contacts:
                    return []

                logger.info(
                    f'Получено {len(contacts)} контактов для юриста {cmd.attorney_id}'
                )
                return [ContactResponse.model_validate(contact) for contact in contacts]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении контактов для юриста с ID {cmd.attorney_id}: {e}'
                )
                raise e
