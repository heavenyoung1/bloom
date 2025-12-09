from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.exceptions import EntityNotFoundException, AccessDeniedException
from backend.application.policy.case_policy import CasePolicy
from backend.application.dto.case import CaseResponse
from backend.application.commands.case import (
    DeleteCaseCommand,
    GetCasesForAttorneyQuery,
)
from backend.core.logger import logger


class GetlAllCasesUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetCasesForAttorneyQuery,
    ) -> bool:
        async with self.uow_factory as uow:
            try:
                # 3. Получить дело
                cases = await uow.client_repo.get_all_for_attorney(cmd.attorney_id)

                logger.info(
                    f'Получено {len(cases)} дел для юриста {cmd.owner_attorney_id}'
                )
                return [CaseResponse.model_validate(case) for case in cases]

            except Exception as e:
                logger.error(
                    f'Ошибка при получении дел для юриста с ID {cmd.owner_attorney_id}: {e}'
                )
                raise e
