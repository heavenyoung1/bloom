from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.policy.case_policy import CasePolicy
from backend.application.commands.case import DeleteCaseCommand
from backend.core.logger import logger


class DeleteCaseUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: DeleteCaseCommand,
    ) -> bool:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидация (проверка уникальности, существования адвоката)
                validator = CasePolicy(
                    attorney_repo=uow.attorney_repo,
                    client_repo=uow.client_repo,
                    case_repo=uow.case_repo,
                )
                await validator.on_delete(cmd)

                # 3. Удалить дело
                await uow.case_repo.delete(cmd.case_id)

                logger.info(f'Дело с ID {cmd.case_id} удалено.')
                return True

            except Exception as e:
                logger.error(f'Ошибка при удалении дела: {e}')
                raise e
