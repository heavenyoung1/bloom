from backend.application.interfaces.repositories.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.interfaces.repositories.case_repo import ICaseRepository
from backend.application.interfaces.repositories.client_repo import IClientRepository
from backend.application.commands.case import (
    CreateCaseCommand,
    UpdateCaseCommand,
    DeleteCaseCommand,
)
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class CasePolicy:
    def __init__(
        self,
        attorney_repo: IAttorneyRepository,
        case_repo: ICaseRepository,
        client_repo: IClientRepository,
    ):
        self.attorney_repo = attorney_repo
        self.case_repo = case_repo
        self.client_repo = client_repo

    async def _check_attorney_exists(self, attorney_id: int) -> None:
        '''Проверить, существует ли адвокат и активен ли он.'''
        attorney = await self.attorney_repo.get(attorney_id)
        if not attorney:
            logger.warning(f'Юрист {attorney_id} не найден')
            raise EntityNotFoundException(f'Юрист не найден')

        if not attorney.is_active:
            logger.warning(f'Юрист не активен: ID={attorney_id}')
            raise ValidationException('Юрист не активен')

        if not attorney.is_verified:
            logger.warning(f'Юрист не верифицирован: ID={attorney_id}')
            raise ValidationException('Юрист не верифицирован')

    async def on_create(self, cmd: CreateCaseCommand) -> None:
        '''Валидировать данные при создании дела'''
        # 1. Проверка, существует ли клиент
        client = await self.client_repo.get(cmd.client_id)
        if not client:
            logger.warning(f'Клиент с ID {cmd.client_id} не найден')
            raise ValidationException(f'Клиент не найден')

        # 2. Проверка, что клиент принадлежит указанному юристу
        if client.owner_attorney_id != cmd.attorney_id:
            logger.error(
                f'Клиент с ID {cmd.client_id} не принадлежит юристу с ID {cmd.attorney_id}'
            )
            raise ValidationException('Клиент не принадлежит юристу')

        # 3. Проверка юриста
        await self._check_attorney_exists(cmd.attorney_id)

    async def on_update(self, cmd: UpdateCaseCommand) -> None:
        # 1. Проверить, что дело существует
        case = await self.case_repo.get(cmd.case_id)
        if not case:
            logger.warning(f'Дело не найдено: ID = {cmd.case_id}')
            raise EntityNotFoundException(f'Дело не найдено')

        # 3. Проверка юриста
        await self._check_attorney_exists(cmd.attorney_id)

    async def on_delete(self, cmd: DeleteCaseCommand) -> None:
        '''Валидировать данные при удалении дела'''
        # 1. Проверить, что дело существует
        case = await self.case_repo.get(cmd.case_id)
        if not case:
            logger.warning(f'Дело не найдено: ID = {cmd.case_id}')
            raise EntityNotFoundException(f'Дело не найдено')

