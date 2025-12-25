from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.dto.case import CaseResponse
from backend.core.exceptions import EntityNotFoundException
from backend.application.commands.case import GetCaseByIdQuery
from backend.core.logger import logger


class GetCaseByIdUseCase:
    '''Сценарий: юрист получает всю информацию по делу.'''
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetCaseByIdQuery,
    ) -> 'CaseResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело
                case = await uow.case_repo.get(cmd.case_id)

                if not case:
                    logger.error(f'Дело с ID {cmd.case_id} не найдено.')
                    raise EntityNotFoundException(f'Дело не найдено.')

                logger.info(f'Дело получено: ID = {cmd.case_id}')
                return CaseResponse.model_validate(case)
            except Exception as e:
                logger.error(f'Ошибка при получении дела: {e}')
                raise e
