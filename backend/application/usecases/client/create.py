from backend.application.dto.client import ClientResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.domain.entities.client import Client
from backend.application.commands.client import CreateClientCommand
from backend.application.policy.client_policy import ClientPolicy
from backend.core.logger import logger


class CreateClientUseCase:
    '''Сценарий: юрист получает создает нового клиента.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreateClientCommand,
    ) -> 'ClientResponse':

        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидация (проверка уникальности, существования адвоката)
                validator = ClientPolicy(
                    client_repo=uow.client_repo,
                    attorney_repo=uow.attorney_repo,
                )
                await validator.on_create(cmd)

                # 2. Создание Entity
                client = Client.create(
                    name=cmd.name,
                    type=cmd.type,
                    email=cmd.email,
                    phone=cmd.phone,
                    personal_info=cmd.personal_info,
                    address=cmd.address,
                    messenger=cmd.messenger,
                    messenger_handle=cmd.messenger_handle,
                    owner_attorney_id=cmd.owner_attorney_id,
                )

                # 3. Сохранение в БД
                saved_client = await uow.client_repo.save(client)

                logger.info(
                    f'Клиент создан: ID = {saved_client.id}'
                    f'Email = {saved_client.email}'
                    f'Владелец = {cmd.messenger_handle}'
                )

                # 4. Возврат Response
                return ClientResponse.model_validate(saved_client)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании клиента: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании клиента: {e}')
                raise Exception('Ошибка при создании клиента')
