from datetime import datetime, timezone
from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.domain.entities.attorney import Attorney
from backend.domain.events.attorney_registered import AttorneyRegisteredEvent
from backend.infrastructure.models.outbox import OutboxEventType
from backend.core.security import SecurityService
from backend.application.policy.attorney_policy import AttorneyPolicy
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.application.commands.attorney import RegisterAttorneyCommand
from backend.application.dto.attorney import AttorneyResponse
from backend.core.logger import logger


class SignUpUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, cmd: RegisterAttorneyCommand) -> 'AttorneyResponse':
        '''
        Регистрация нового юриста.

        Flow:
        1. Валидировать данные через Policy
        2. Захешировать пароль
        3. Создать Entity
        4. Сохранить в БД
        '''
        async with self.uow_factory.create() as uow:
            try:
                # 1. Валидировать
                policy = AttorneyPolicy(uow.attorney_repo)
                await policy.on_register(cmd)

                # 2. Захешировать пароль
                hashed_password = SecurityService.hash_password(cmd.password)

                # 3. Создать Entity
                attorney = Attorney.create(
                    license_id=cmd.license_id,
                    first_name=cmd.first_name,
                    last_name=cmd.last_name,
                    patronymic=cmd.patronymic,
                    email=cmd.email,
                    phone=cmd.phone,
                    hashed_password=hashed_password,
                    telegram_username=cmd.telegram_username,
                )

                # 4. Сохранить в БД
                attorney = await uow.attorney_repo.save(attorney)

                # 5. Создать доменное событие и сохранить в Outbox
                # (в той же транзакции для гарантии доставки)
                event = AttorneyRegisteredEvent(
                    attorney_id=attorney.id,
                    email=attorney.email,
                    first_name=attorney.first_name,
                    occurred_at=datetime.now(timezone.utc),
                )

                await uow.outbox_repo.save_event(
                    event_type=OutboxEventType.ATTORNEY_REGISTERED.value,
                    payload=event.to_dict(),
                )

                logger.info(
                    f'[OUTBOX] Событие регистрации сохранено для {attorney.email}'
                )

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка валидации при регистрации: {e}')
                raise

        logger.info(
            f'Юрист зарегистрирован: {attorney.email} '
            f'(ID: {attorney.id}). Ожидание верификации...'
        )

        # Создаем DTO напрямую из доменной сущности (быстрее чем model_validate)
        return AttorneyResponse(
            id=attorney.id,
            email=attorney.email,
            is_active=attorney.is_active,
            is_superuser=attorney.is_superuser,
            is_verified=attorney.is_verified,
            license_id=attorney.license_id,
            first_name=attorney.first_name,
            last_name=attorney.last_name,
            patronymic=attorney.patronymic,
            phone=attorney.phone,
            telegram_username=attorney.telegram_username,
            created_at=attorney.created_at,
            updated_at=attorney.updated_at,
        )
