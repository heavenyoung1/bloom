import random
import string
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys
from backend.infrastructure.email.email_service import EmailService
from backend.core.exceptions import ValidationException
from backend.core.logger import logger


class VerificationService:
    '''Сервис для управления верификацией email'''

    @staticmethod
    def generate_code(length: int = 6) -> str:
        '''
        Сгенерировать код верификации.

        TODO: Использовать secrets вместо random для большей безопасности
        '''
        code =  ''.join(random.choices(string.digits, k=length))
        logger.debug(f'[TEST] КОД СГЕНЕРИРОВАН! {code}')
        return code

    @staticmethod
    async def send_verification_code(email: str, first_name: str) -> bool:
        '''
        Отправить код верификации на email.

        Используется в: SignUpUseCase, ResendVerificationUseCase

        Args:
            email: Email адвоката
            first_name: Имя для письма

        Returns:
            True если письмо отправлено успешно
        '''
        # 1. Генерируем код
        code = VerificationService.generate_code()

        # 2. Сохраняем в Redis на 15 минут
        await redis_client.set(
            RedisKeys.email_verification_code(email), code, ttl=15 * 60  # 15 минут
        )

        logger.info(f'[VERIFICATION] Код верификации сгенерирован для {email}')

        # 3. Отправляем письмо
        return await EmailService.send_verification_email(
            email=email, verification_code=code, first_name=first_name
        )

    @staticmethod
    async def verify_code(email: str, code: str) -> bool:
        '''
        Проверить введённый код верификации.

        Используется в: VerifyEmailUseCase

        Args:
            email: Email адвоката
            code: Код который ввел пользователь

        Returns:
            True если код правильный, False если неправильный или истек

        Raises:
            ValidationException: Если код не найден (это обычно нормально)
        '''
        # 1. Получаем код из Redis
        stored_code = await redis_client.get(RedisKeys.email_verification_code(email))

        if stored_code is None:
            logger.warning(f'[VERIFICATION] Код не найден или истек для {email}')
            return False

        # 2. Нормализуем типы (Redis может вернуть bytes)
        stored_code = str(stored_code).strip()
        code = str(code).strip()

        # 3. Сравниваем коды
        if stored_code != code:
            logger.warning(f'[VERIFICATION] Неправильный код для {email}')
            return False

        logger.info(f'[VERIFICATION] Код подтверждён для {email}')
        return True

    @staticmethod
    async def cleanup_code(email: str) -> None:
        '''
        Удалить код верификации из Redis.

        Используется в: VerifyEmailUseCase (после успешной верификации)

        Args:
            email: Email адвоката
        '''
        await redis_client.delete(RedisKeys.email_verification_code(email))
        logger.debug(f'[VERIFICATION] Код удален для {email}')
