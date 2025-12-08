from backend.infrastructure.repositories.interfaces.client_repo import (
    IClientRepository,
)
from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientCreateRequest, ClientUpdateRequest
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class ClientPolicy:
    '''Валидатор для клиентов.'''

    def __init__(
        self, client_repo: IClientRepository, attorney_repo: IAttorneyRepository
    ):
        self.client_repo = client_repo  # Репозиторий для клиентов
        self.attorney_repo = attorney_repo  # Репозиторий для адвокатов

    async def _check_attorney_exists(self, attorney_id: int) -> None:
        '''Проверить, существует ли адвокат и активен ли он.'''
        attorney = await self.attorney_repo.get(attorney_id)
        if not attorney:
            logger.warning(f'Юрист {attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {attorney_id} не найден')

        if not attorney.is_active:
            logger.warning(f'Юрист не активен: ID={attorney_id}')
            raise ValidationException('Attorney account is not active')

        if not attorney.is_verified:
            logger.warning(f'Юрист не верифицирован: ID={attorney_id}')
            raise ValidationException('Attorney account is not verified')

    async def _check_unique_field(
        self,
        field_value: str,
        field_name: str,
        owner_attorney_id: int,
        client_id: int = None,
    ) -> None:
        '''Проверка уникальности поля для клиента (email, phone, personal_info)'''
        if field_name == 'email':
            existing = await self.client_repo.get_by_email_for_owner(
                field_value, owner_attorney_id
            )
        elif field_name == 'phone':
            existing = await self.client_repo.get_by_phone_for_owner(
                field_value, owner_attorney_id
            )
        elif field_name == 'personal_info':
            existing = await self.client_repo.get_by_personal_info_for_owner(
                field_value, owner_attorney_id
            )
        else:
            raise ValidationException(f'Unknown field {field_name}')

        if existing and (client_id is None or existing.id != client_id):
            logger.warning(
                f'{field_name.capitalize()} {field_value} уже используется клиентом ID={existing.id} у юриста {owner_attorney_id}'
            )
            raise ValidationException(
                f'{field_name.capitalize()} {field_value} уже используется другим клиентом этого юриста'
            )

    async def on_create(
        self, request: ClientCreateRequest, owner_attorney_id: int
    ) -> None:
        '''Валидировать данные при создании клиента.'''

        # 1. Проверка существования адвоката
        await self._check_attorney_exists(owner_attorney_id)

        # 2. Проверки уникальности полей
        if request.email:
            await self._check_unique_field(request.email, 'email', owner_attorney_id)
        if request.phone:
            await self._check_unique_field(request.phone, 'phone', owner_attorney_id)
        if request.personal_info:
            await self._check_unique_field(
                request.personal_info, 'personal_info', owner_attorney_id
            )

    async def on_update(
        self, request: ClientUpdateRequest, owner_attorney_id: int, client_id: int
    ) -> None:
        '''Валидировать при обновлении (проверить уникальность)'''

        # Проверка только тех полей, которые изменяются
        if request.email:
            await self._check_unique_field(
                request.email, 'email', owner_attorney_id, client_id
            )
        if request.phone:
            await self._check_unique_field(
                request.phone, 'phone', owner_attorney_id, client_id
            )
        if request.personal_info:
            await self._check_unique_field(
                request.personal_info, 'personal_info', owner_attorney_id, client_id
            )
