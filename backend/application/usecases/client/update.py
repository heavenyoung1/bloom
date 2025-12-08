from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientUpdateRequest, ClientResponse
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.application.policy.client_policy import ClientPolicy
from backend.application.commands.client import UpdateClientCommand
from backend.core.logger import logger


class UpdateClientUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdateClientCommand,
    ) -> ClientResponse:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить клиента
                client = await uow.attorney_repo.get(cmd.client_id)
                if not client:
                    logger.warning(f'Клиент не найден: ID = {cmd.client_id}')
                    raise EntityNotFoundException(
                        f'Клиент не найден: ID = {cmd.client_id}'
                    )

                # 2. Валидация бизнес-правил (уникальность и т.п.)
                policy = ClientPolicy(
                    client_repo=uow.client_repo,
                    attorney_repo=uow.attorney_repo,
                )
                await policy.on_update(cmd)

                # 2. Применяем изменения через метод update доменной сущности
                client.update(cmd)

                # 3. Сохраняем изменения
                updated_client = await uow.client_repo.save(client)

                logger.info(f'Клиент обновлён: ID = {updated_client.id}')

                return ClientResponse.model_validate(updated_client)

            except Exception as e:
                logger.error(f'Ошибка при обновлении клиента: {e}')
                # Можно не заворачивать, а просто пробросить
                raise
