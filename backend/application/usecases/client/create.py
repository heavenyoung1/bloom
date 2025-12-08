from backend.application.dto.client import ClientCreateRequest, ClientResponse
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.domain.entities.client import Client
from backend.application.policy.client_policy import ClientPolicy
from backend.core.logger import logger


class CreateClientUseCase:
    '''
    Создание нового клиента

    Ответственность:
    - Координация валидации, создания и сохранения
    - Обработка ошибок
    - Логирование
    '''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        request: ClientCreateRequest,
        owner_attorney_id: int,  # Из JWT!
    ) -> 'ClientResponse':

        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидация (проверка уникальности, существования адвоката)
                validator = ClientPolicy(
                    client_repo=uow.client_repo, attorney_repo=uow.attorney_repo
                )
                await validator.on_create(request, owner_attorney_id)

                # 2. Создание Entity
                client = Client.create(
                    name=request.name,
                    type=request.type,
                    email=request.email,
                    phone=request.phone,
                    personal_info=request.personal_info,
                    address=request.address,
                    messenger=request.messenger,
                    messenger_handle=request.messenger_handle,
                    owner_attorney_id=owner_attorney_id,
                )

                # 3. Сохранение в БД
                saved_client = await uow.client_repo.save(client)

                logger.info(
                    f'Клиент создан: ID = {saved_client.id}'
                    'Email = {saved_client.email}'
                    'Владелец = {owner_attorney_id}'
                )

                # 4. Возврат Response
                return ClientResponse.model_validate(saved_client)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании клиента: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании клиента: {e}')
                raise Exception('Ошибка при создании клиента')
