from backend.infrastructure.repositories.interfaces.client_repo import (
    IClientRepository,
)
from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.dto.client import (ClientCreateRequest)
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class ClientValidator:
    '''Валидатор для клиентов.'''

    def __init__(
        self,
        client_repo: IClientRepository,
        attorney_repo: IAttorneyRepository,
    ):
        self.client_repo = client_repo
        self.attorney_repo = attorney_repo

    async def on_create(self, dto: ClientCreateRequest) -> None:
        '''Валидировать данные при создании клиента.'''

        owner_id = dto.owner_attorney_id

        # 1. Юрист должен существовать
        attorney = await self.attorney_repo.get(owner_id)
        if not attorney:
            logger.warning(f'Юрист {owner_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {owner_id} не найден')

        # 2. Email должен быть уникален для этого юриста (если указан)
        if dto.email:
            existing = await self.client_repo.get_by_email_for_owner(dto.email, owner_id)
            if existing:
                logger.warning(
                    f'Email {dto.email} уже используется клиентом ID={existing.id} у юриста {owner_id}'
                )
                raise ValidationException(
                    f'Email {dto.email} уже используется другим клиентом этого юриста'
                )

        # 3. Телефон должен быть уникален для этого юриста
        existing = await self.client_repo.get_by_phone_for_owner(dto.phone, owner_id)
        if existing:
            logger.warning(
                f'Телефон {dto.phone} уже используется клиентом ID={existing.id} у юриста {owner_id}'
            )
            raise ValidationException(
                f'Телефон {dto.phone} уже используется другим клиентом этого юриста'
            )

        # 4. personal_info должен быть уникален для этого юриста
        existing = await self.client_repo.get_by_personal_info_for_owner(
            dto.personal_info, owner_id
        )
        if existing:
            logger.warning(
                f'personal_info {dto.personal_info} уже используется клиентом ID={existing.id} у юриста {owner_id}'
            )
            raise ValidationException(
                f'Документ/ИНН {dto.personal_info} уже используется другим клиентом этого юриста'
            )