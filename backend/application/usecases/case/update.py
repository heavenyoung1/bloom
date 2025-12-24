from backend.application.dto.case import CaseResponse
from backend.domain.entities.case import Case
from backend.domain.entities.auxiliary import CaseStatus
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.case import UpdateCaseCommand
from backend.application.policy.case_policy import CasePolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class UpdateCaseUseCase:
    '''Сценарий: юрист создаёт новое дело.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: UpdateCaseCommand,
    ) -> 'CaseResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Получить дело
                case = await uow.case_repo.get(cmd.case_id)
                if not case:
                    logger.warning(f'Дело не найден: ID = {cmd.client_id}')
                    raise EntityNotFoundException(
                        f'Дело не найден: ID = {cmd.client_id}'
                    )

                # 1. Валидация (проверка уникальности, существования адвоката)
                validator = CasePolicy(
                    attorney_repo=uow.attorney_repo,
                    client_repo=uow.client_repo,
                    case_repo=uow.case_repo,
                )
                await validator.on_update(cmd)

                # 2. Применяем изменения через метод update доменной сущности
                case.update(cmd)

                # 3. Сохранение в базе
                updated_case = await uow.case_repo.update(case)

                logger.info(
                    f'Дело обновлено: ID = {updated_case.id}'
                    f'Владелец = {updated_case.attorney_id}'
                    f'Связанный клиент = {updated_case.client_id}'
                )

                # 4. Возврат Response
                return CaseResponse.model_validate(updated_case)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при обновлении дела: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при обновлении дела: {e}')
                raise Exception('Ошибка при обновлении дела')
