from backend.application.dto.case import CaseCreateRequest, CaseResponse
from backend.domain.entities.case import Case
from backend.domain.entities.auxiliary import CaseStatus
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.case import CreateCaseCommand
from backend.application.policy.case_policy import CasePolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class CreateCaseUseCase:
    '''Сценарий: юрист создаёт новое дело.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
        self,
        cmd: CreateCaseCommand,
    ) -> 'CaseResponse':
        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидация (проверка уникальности, существования юриста)
                validator = CasePolicy(
                    attorney_repo=uow.attorney_repo,
                    client_repo=uow.client_repo,
                    case_repo=uow.case_repo,
                )
                await validator.on_create(cmd)

                # 2. Создание Entity
                case = Case.create(
                    name=cmd.name,
                    client_id=cmd.client_id,
                    attorney_id=cmd.attorney_id,
                    status=cmd.status,  # Статус будет передан из команды
                    description=cmd.description,
                )

                # 3. Сохранение в базе
                saved_case = await uow.case_repo.save(case)

                logger.info(
                    f'Дело создано: ID = {saved_case.id} '
                    f'Владелец = {saved_case.attorney_id} '
                    f'Связанный клиент = {saved_case.client_id} '
                )

                # 4. Возврат Response
                return CaseResponse.model_validate(saved_case)

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка при создании клиента: {e}')
                raise e  # Пробрасываем ошибку дальше

            except Exception as e:
                logger.error(f'Неизвестная ошибка при создании клиента: {e}')
                raise Exception('Ошибка при создании клиента')
