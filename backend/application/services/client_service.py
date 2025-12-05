from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory

# from backend.application.usecases.client import (
#     CreateClientUseCase,
#     # UpdateClientUseCase,
#     # DeleteClientUseCase,
#     # GetClientByIdUseCase,
#     # GetClientsForAttorneyUseCase,
# )

from backend.application.validators.client_validator import ClientValidator
from backend.application.usecases.client.create import CreateClientUseCase

from backend.application.dto.client import (
    ClientCreateRequest,
    ClientResponse,
)

from backend.core.exceptions import (
    NotFoundException,
    VerificationError,
    AccessDeniedException,
)

from backend.core.logger import logger


class ClientService:
    '''
    Сервис для работы с клиентами

    Ответственность:
    - Координация различных UseCase'ов
    - Может добавить дополнительную логику (логирование, кэширование и т.д.)
    '''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        # Инициализируем все UseCase'ы
        self.create_client_use_case = CreateClientUseCase(uow_factory)
        # self.get_client_use_case = GetClientUseCase(uow_factory)
        # self.update_client_use_case = UpdateClientUseCase(uow_factory)
        # self.delete_client_use_case = DeleteClientUseCase(uow_factory)
        # self.list_clients_use_case = ListClientsUseCase(uow_factory)

    # ========== CHECK ACCESS ==========

    async def _check_owner_access(
        self, current_attorney_id: int, owner_attorney_id: int
    ):
        '''Проверка прав доступа владельца'''
        if current_attorney_id != owner_attorney_id:
            raise AccessDeniedException(
                "You are not authorized to access this client's data."
            )

    # ========== CREATE CLIENT ==========

    async def create_client(
        self, request, owner_attorney_id: int, current_attorney_id: int
    ):

        # Проверяем права доступа владельца
        await self._check_owner_access(current_attorney_id, owner_attorney_id)

        # Вызываем UseCase
        return await self.create_client_use_case.execute(request, owner_attorney_id)


# # ========== UPDATE CLIENT ==========

#     async def update_client(self, request, owner_attorney_id: int, current_attorney_id: int):

#         # Проверяем права доступа владельца
#         self._check_owner_access(current_attorney_id, owner_attorney_id)

#         # Вызываем UseCase
#         return await self.update_client_use_case.execute(request, owner_attorney_id)

# # ========== DELETE CLIENT ==========

#     async def delete_client(self, request, owner_attorney_id: int, current_attorney_id: int):

#         # Проверяем права доступа владельца
#         self._check_owner_access(current_attorney_id, owner_attorney_id)

#         # Вызываем UseCase
#         return await self.delete_client_use_case.execute(request, owner_attorney_id)

# # ========== GET ONE CLIENT ==========

#     async def get_client_by_id(self, request, owner_attorney_id: int, current_attorney_id: int):

#         # Проверяем права доступа владельца
#         self._check_owner_access(current_attorney_id, owner_attorney_id)

#         # Вызываем UseCase
#         return await self.get_client_by_id_use_case.execute(request, owner_attorney_id)

# # ========== GET ALL CLIENTS FOR ATTORNEY ==========

#     async def get_all_clients(self, request, owner_attorney_id: int, current_attorney_id: int):

#         # Проверяем права доступа владельца
#         self._check_owner_access(current_attorney_id, owner_attorney_id)

#         # Вызываем UseCase
#         return await self.get_clients_for_attorney_use_case.execute(
#             request, owner_attorney_id
#         )
