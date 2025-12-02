import random
import string
from backend.infrastructure.redis.client import redis_client
from backend.infrastructure.redis.keys import RedisKeys
from backend.infrastructure.email.email_service import EmailService
from backend.infrastructure.repositories.attorney_repo import AttorneyRepository
from backend.core.logger import logger


class VerificationService:
    '''Сервис для управления верификацией email'''

    @staticmethod
    def generate_code(length: int = 6) -> str:
        '''Сгенерировать 6-значный код'''
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    async def send_verification_code(email: str, first_name: str) -> bool:
        '''Отправить код верификации на email'''

        # Генерируем код
        code = VerificationService.generate_code()

        # Сохраняем в Redis на 15 минут
        await redis_client.set(
            RedisKeys.email_verification_code(email), code, ttl=15 * 60  # 15 минут
        )

        logger.info(f'[VERIFICATION] Код отправлен на {email}: {code}')

        # Отправляем email
        return await EmailService.send_verification_email(
            email=email, verification_code=code, first_name=first_name
        )

    @staticmethod
    async def verify_code(email: str, code: str) -> bool:
        '''Проверить введённый код'''

        # Получаем код из Redis
        stored_code = await redis_client.get(RedisKeys.email_verification_code(email))

        if stored_code is None:
            logger.warning(f'[VERIFICATION] Код не найден для {email}')
            return False

        if stored_code != code:
            logger.warning(f'[VERIFICATION] Неправильный код для {email}')
            return False

        logger.info(f'[VERIFICATION] Код подтвержден для {email}')
        return True

    @staticmethod
    async def mark_email_as_verified(
        attorney_repo: AttorneyRepository, email: str
    ) -> None:
        '''Отметить email как подтвержденный'''

        attorney = await attorney_repo.get_by_email(email)
        if attorney:
            # ⚠️ Нужно обновить ORM напрямую, т.к. domain entity не изменяет БД
            # Это временное решение - лучше создать метод update в репозитории
            attorney.is_verified = True

            # ХУЙНЯЯЯ!!!⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
            # ХУЙНЯЯЯ!!!⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
            # ХУЙНЯЯЯ!!!⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
            # ХУЙНЯЯЯ!!!⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
            await attorney_repo.session.commit()
            logger.info(f'[VERIFICATION] Email подтвержден для {email}')

    @staticmethod
    async def cleanup_code(email: str) -> None:
        '''Удалить код после успешной верификации'''
        await redis_client.delete(RedisKeys.email_verification_code(email))
