from backend.application.dto.case import CaseResponse
from backend.application.commands.case import GetCasesForAttorneyQuery
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.core.logger import logger

from typing import List


class GetlAllCasesUseCase:
    '''Сценарий: юрист получает все дела.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: GetCasesForAttorneyQuery,
    ) -> List['CaseResponse']:
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получаем ORM объекты с загруженными связями
                orm_cases = await uow.case_repo.get_all_for_attorney_with_relations(
                    cmd.attorney_id
                )
                if not orm_cases:
                    logger.info(f'Нет дел для юриста с ID {cmd.attorney_id}')
                    return []

                # 3. Маппим каждый ORM объект в DTO
                # Pydantic автоматически обработает вложенные client и contacts
                case_responses = [
                    CaseResponse.model_validate(orm_case) for orm_case in orm_cases
                ]

                logger.info(
                    f'Получено {len(case_responses)} дел для юриста {cmd.attorney_id}'
                )

                return case_responses

            except Exception as e:
                logger.error(
                    f'Ошибка при получении дел для юриста с ID {cmd.attorney_id}: {e}'
                )
                raise e


# ПРОШЛАЯ РЕАЛИЗАЦИЯ!!!
# class GetlAllCasesUseCase:
#     def __init__(self, uow_factory: UnitOfWorkFactory):
#         self.uow_factory = uow_factory

#     async def execute(
#         self,
#         cmd: GetCasesForAttorneyQuery,
#     ) -> bool:
#         async with self.uow_factory.create() as uow:
#             try:
#                 # 1. Получить все дела для указанного юриста
#                 cases = await uow.case_repo.get_all_for_attorney(cmd.attorney_id)

#                 # Проверка, что дела существуют
#                 if not cases:
#                     logger.warning(f'Нет дел для юриста с ID {cmd.attorney_id}')
#                     raise EntityNotFoundException(
#                         f'Нет дел для юриста с ID {cmd.attorney_id}'
#                     )

#                 logger.info(f'Получено {len(cases)} дел для юриста {cmd.attorney_id}')
#                 # 2. Возвращаем список дел в нужном формате (через модель CaseResponse)
#                 case_responses = [
#                     CaseResponse(
#                         id=case.id,
#                         name=case.name,
#                         client_id=case.client_id,  # Здесь должны быть данные клиента
#                         attorney_id=case.attorney_id,  # Здесь должны быть данные адвоката
#                         status=case.status,
#                         description=case.description,
#                         created_at=case.created_at,
#                         updated_at=case.updated_at,
#                     )
#                     for case in cases
#                 ]

#                 logger.info(
#                     f'Получено {len(cases)} дел для юриста с ID {cmd.attorney_id}'
#                 )
#                 return case_responses

#             except Exception as e:
#                 logger.error(
#                     f'Ошибка при получении дел для юриста с ID {cmd.attorney_id}: {e}'
#                 )
#                 raise e
