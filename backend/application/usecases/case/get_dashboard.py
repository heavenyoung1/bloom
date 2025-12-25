from backend.application.dto.case import DashboardResponse
from backend.application.commands.case import GetDashboardQuery
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.logger import logger

from typing import List


class GetDashboardUseCase:
    '''Сценарий: получение данных дашборда для адвоката.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetDashboardQuery,
    ) -> List['DashboardResponse']:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получаем данные дашборда из репозитория
                dashboard_data = await uow.case_repo.get_dashboard_data(cmd.attorney_id)

                if not dashboard_data:
                    logger.info(f'Нет данных для дашборда адвоката с ID {cmd.attorney_id}')
                    return []

                # 2. Преобразуем словари в DTO
                dashboard_responses = [
                    DashboardResponse(**data) for data in dashboard_data
                ]

                logger.info(
                    f'Получено {len(dashboard_responses)} записей для дашборда '
                    f'адвоката {cmd.attorney_id}'
                )

                return dashboard_responses

            except Exception as e:
                logger.error(
                    f'Ошибка при получении данных дашборда для адвоката '
                    f'с ID {cmd.attorney_id}: {e}'
                )
                raise e

