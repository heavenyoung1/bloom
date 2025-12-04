from backend.infrastructure.repositories.interfaces.client_repo import (
    IClientRepository,
)
from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.dto.client import ClientCreateRequest, ClientUpdateRequest
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class ClientValidator:
    '''
    Валидатор для клиентов.
    
    Ответственность:
    - Проверка существования владельца (адвоката)
    - Проверка уникальности полей (email, phone, personal_info)
    - Проверка корректности данных
    '''

    def __init__(
        self,
        client_repo: IClientRepository,
        attorney_repo: IAttorneyRepository,
    ):
        self.client_repo = client_repo
        self.attorney_repo = attorney_repo

    async def on_create(
        self,
        request: ClientCreateRequest,
        owner_attorney_id: int,  # Из JWT, не из DTO!
    ) -> None:
        '''
        Валидировать данные при создании клиента.
        
        Проверки:
        1. Адвокат существует и активен
        2. Email уникален для этого адвоката (если указан)
        3. Телефон уникален для этого адвоката
        4. Personal_info (ИНН/паспорт) уникален для этого адвоката
        
        Args:
            request: ClientCreateRequest
            owner_attorney_id: ID владельца (адвоката)
            
        Raises:
            EntityNotFoundException: Адвокат не найден
            ValidationException: Нарушение бизнес-правил
        '''

        # 1. Юрист должен существовать
        attorney = await self.attorney_repo.get(owner_attorney_id)

        if not attorney:
            logger.warning(f'Юрист {owner_attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист с ID {owner_attorney_id} не найден')

        # Проверить что юрист активен
        if not attorney.is_active:
            logger.warning(f"Attorney is not active: ID={owner_attorney_id}")
            raise ValidationException(
                "Attorney account is not active"
            )
        
        # Проверить что адвокат верифицирован
        if not attorney.is_verified:
            logger.warning(f"Attorney is not verified: ID={owner_attorney_id}")
            raise ValidationException(
                "Attorney account is not verified"
            )

        # ========== ПРОВЕРКА 2: Email уникален (если указан) ==========
        if request.email:
            existing = await self.client_repo.get_by_email_for_owner(
                request.email, owner_attorney_id
            )
            if existing:
                logger.warning(
                    f'Email {request.email} уже используется клиентом ID={existing.id} у юриста {owner_attorney_id}'
                )
                raise ValidationException(
                    f'Email {request.email} уже используется другим клиентом этого юриста'
                )

        # ========== ПРОВЕРКА 3: Телефон уникален ==========
        existing = await self.client_repo.get_by_phone_for_owner(
            request.phone, 
            owner_attorney_id,
        )
        if existing:
            logger.warning(
                f'Телефон {request.phone} уже используется клиентом ID={existing.id} у юриста {owner_attorney_id}'
            )
            raise ValidationException(
                f'Телефон {request.phone} уже используется другим клиентом этого юриста'
            )

        # ========== ПРОВЕРКА 4: Personal_info (ИНН/паспорт) уникален ==========
        existing = await self.client_repo.get_by_personal_info_for_owner(
            request.personal_info, 
            owner_attorney_id,
        )
        if existing:
            logger.warning(
                f'personal_info {request.personal_info} уже используется клиентом ID={existing.id} у юриста {owner_attorney_id}'
            )
            raise ValidationException(
                f'Документ/ИНН {request.personal_info} уже используется другим клиентом этого юриста'
            )
        
    
    async def on_update(
        self,
        request: ClientUpdateRequest,
        owner_attorney_id: int,
        client_id: int,  # Исключить текущего клиента
    ) -> None:
        """Валидировать при обновлении (проверить уникальность)"""
        # Проверить только поля которые изменяются
        if request.phone:
            existing = await self.client_repo.get_by_phone_for_owner(
                request.phone, owner_attorney_id
            )
            if existing and existing.id != client_id:  # Исключить текущего
                raise ValidationException(f"Phone already used")
        # Аналогично для email и personal_info