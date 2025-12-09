from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.policy.client_policy import ClientPolicy
from backend.application.commands.case import (
    CreateCaseCommand,
    UpdateCaseCommand,
    DeleteCaseCommand,
    GetCaseByIdQuery,
    GetCasesForAttorneyQuery,
)
from backend.application.dto.case import (
    CaseCreateRequest,
    CaseResponse,
)
from backend.application.usecases.case import (
    CreateCaseUseCase,
    UpdateCaseUseCase,
    DeleteCaseUseCase,
    GetCaseByIdUseCase,
    GetlAllCasesUseCase,
)

from backend.core.logger import logger




from backend.core.exceptions import (
    NotFoundException,
    VerificationError,
    AccessDeniedException,
)

class CaseService:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        # Инициализируем все UseCase'ы
        self.create_case_use_case = CreateCaseUseCase(uow_factory)
        self.update_case_use_case = UpdateCaseUseCase(uow_factory)
        self.delete_case_use_case = DeleteCaseUseCase(uow_factory)
        self.get_case_use_case = GetCaseByIdUseCase(uow_factory)
        self.list_cases_use_case = GetlAllCasesUseCase(uow_factory)

    # ========== CHECK ACCESS ==========

    async def _check_owner_access(
        self,
        current_attorney_id: int,
        owner_attorney_id: int,
    ):
        '''Проверка прав доступа владельца'''
        if owner_attorney_id != current_attorney_id:
            logger.warning(f'ACCESS DENIED: У ВАС НЕТ ДОСТУПА К ЭТОЙ СУЩНОСТИ!')
            raise AccessDeniedException(
                'ACCESS DENIED: У ВАС НЕТ ДОСТУПА К ЭТОЙ СУЩНОСТИ!'
            )

    # ========== CREATE CLIENT ==========

    async def create_client(self, cmd: CreateCaseCommand):
        return await self.create_case_use_case.execute(cmd)

    # ========== UPDATE CLIENT ==========

    async def update_client(
        self, cmd: UpdateCaseCommand, owner_attorney_id: int, current_attorney_id: int
    ):
        self._check_owner_access(current_attorney_id, owner_attorney_id)

        return await self.update_case_use_case.execute(cmd)

    # ========== DELETE CLIENT ==========

    async def delete_client(
        self, cmd: DeleteCaseCommand, owner_attorney_id: int, current_attorney_id: int
    ):
        self._check_owner_access(current_attorney_id, owner_attorney_id)

        return await self.delete_case_use_case.execute(cmd)

    # ========== GET ONE CLIENT ==========

    async def get_client_by_id(
        self, client_id, owner_attorney_id: int, current_attorney_id: int
    ):
        self._check_owner_access(current_attorney_id, owner_attorney_id)

        # Создаём команду для получения клиента по ID
        cmd = GetCaseByIdQuery(client_id)

        # Передаем команду в use case
        return await self.get_case_use_case.execute(cmd)

    # ========== GET ALL CLIENTS FOR ATTORNEY ==========

    async def get_all_clients(
        self,
        cmd: GetCasesForAttorneyQuery,
        owner_attorney_id: int,
        current_attorney_id: int,
    ):
        self._check_owner_access(current_attorney_id, owner_attorney_id)
        return await self.list_cases_use_case.execute(cmd)