from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientUpdateRequest, ClientResponse
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.core.logger import logger


class UpdateClientUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self, client_id: int, request: ClientUpdateRequest, attorney_id: int
    ) -> ClientResponse:
        async with self.uow_factory as uow:
            try:
                # Валидация
                # ДОБАВИТЬ ВАЛИДАЦИЮ ДЛЯ ОБНОВЛЕНИЯ
                # validator = ClientValidator(client_repo=uow.client_repo)
                # await validator.on_update(client_id, request)

                # 1. Получить клиента
                client = await uow.client_repo.get(client_id)
                if not client:
                    logger.warning(f"Client not found: ID={client_id}")
                    raise EntityNotFoundException(f'Клиент с ID {client_id} не найден.')

                # 2. Проверить права доступа
                if client.owner_attorney_id != attorney_id:
                    logger.warning(
                        f"Access denied: Attorney {attorney_id} tried to update "
                        f"client {client_id} owned by {client.owner_attorney_id}"
                    )
                    raise AccessDeniedException("You don't have access to this client")

                # Обновление данных
                # ВОТ ЭТО КОНЕЧНО ПОЛНОЕ ДЕРЬМО
                client.name = request.name
                client.type = request.type
                client.email = request.email
                client.phone = request.phone
                client.address = request.address
                client.messenger = request.messenger
                client.messenger_handle = request.messenger_handle
                client.personal_info = request.personal_info

                # Сохранение изменений
                updated_client = await uow.client_repo.save(client)

                logger.info(f'Клиент обновлён: ID = {updated_client.id}')

                return ClientResponse.model_validate(updated_client)

            except Exception as e:
                logger.error(f'Ошибка при обновлении клиента: {e}')
                raise e
