from backend.application.interfaces.repositories.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.interfaces.repositories.client_repo import IClientRepository
from backend.application.commands.client import (
    CreateClientCommand,
    UpdateClientCommand,
)

from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.client import ClientCreateRequest, ClientUpdateRequest
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class ClientPolicy:
    '''Валидатор для клиентов.'''

    def __init__(
        self,
        client_repo: IClientRepository,
        attorney_repo: IAttorneyRepository,
    ):
        self.attorney_repo = attorney_repo
        self.client_repo = client_repo

    # ТУТ МОЖНО БУДЕТ ПОЗЖЕ ДОБАВИТЬ НОВУЮ ЛОГИКУ!!!
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

    async def on_create(self, cmd: CreateClientCommand) -> None:
        '''Валидировать данные при создании клиента.'''

        # 1. Проверка адвоката
        await self._check_attorney_exists(cmd.owner_attorney_id)

        # 2. Уникальность
        if cmd.email:
            await self._check_unique_field(cmd.email, 'email', cmd.owner_attorney_id)
        if cmd.phone:
            await self._check_unique_field(cmd.phone, 'phone', cmd.owner_attorney_id)
        if cmd.personal_info:
            await self._check_unique_field(
                cmd.personal_info, 'personal_info', cmd.owner_attorney_id
            )

    async def on_update(self, cmd: UpdateClientCommand) -> None:
        '''Валидировать при обновлении (проверить уникальность)'''
        pass
