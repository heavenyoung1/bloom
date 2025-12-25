import pytest
from unittest.mock import AsyncMock, patch
from backend.core.logger import logger


@pytest.fixture(autouse=True)
async def mock_email_service():
    '''
    Замокировать EmailService для тестов.

    autouse=True означает, что мок применяется ко всем тестам автоматически.

    Что делает:
    - Перехватывает попытки отправки писем
    - Вместо отправки просто логирует и возвращает True
    - Это позволяет коду верификации сохраняться в Redis без ошибок
    '''

    # Создаем асинхронный мок функции
    mock_send_email = AsyncMock(return_value=True)

    # Патчим реальный EmailService.send_verification_email
    # НУ МНЕ ЭТО НЕ ОЧЕНЬ НРАВИТСЯ КАК ТО ВООБЩЕ
    with patch(
        'backend.infrastructure.email.email_service.EmailService.send_verification_email',
        new=mock_send_email,
    ):
        logger.info('[MOCK] EmailService замокирован')
        yield mock_send_email
        logger.info('[MOCK] EmailService демокирован')
