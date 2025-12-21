from backend.infrastructure.tools.uow_factory import UnitOfWorkFactory
from backend.application.commands.attorney import ForgotPasswordCommand
from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.domain.events.attorney_registered import AttorneyRegisteredEvent
from backend.infrastructure.models.outbox import OutboxEventType
from backend.application.services.token_management_service import TokenManagementService
from datetime import datetime, timezone

from backend.core.logger import logger


class ForgotPasswordUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        token_service: TokenManagementService,
    ):
        self.uow_factory = uow_factory
        self.token_service = token_service

    async def execute(self, cmd: ForgotPasswordCommand):

        # 1. Проверить rate limiting (БЕЗ UoW - это просто Redis)
        await self.token_service.check_rate_limit(cmd.email)

        async with self.uow_factory.create() as uow:
            try:

                # 2. Получить юриста по email
                attorney = await uow.attorney_repo.get_by_email(cmd.email)
                if not attorney:
                    # Записать попытку
                    await self.token_service.record_failed_attempt(cmd.email)
                    raise ValidationException('Некорректный email или пароль')

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
                    f'[OUTBOX] Событие сброса пароля сохранено для {attorney.email}'
                )

                logger.info(
                    f'Код для сброса пароля будет отправлен: {attorney.email} '
                    f'(ID: {attorney.id}). Ожидание сброса пароля...'
                )

            except (ValidationException, EntityNotFoundException) as e:
                logger.error(f'Ошибка валидации при сбросе пароля: {e}')
                raise
