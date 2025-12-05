from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
import jwt
from backend.core.settings import settings
from backend.core.logger import logger

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class SecurityService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # ========== JWT TOKEN CREATION ==========

    @staticmethod
    def create_access_token(
        subject: str,
        expires_delta: Optional[timedelta] = None,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        '''
        Создать ACCESS TOKEN (короткоживущий, для API запросов).

        Используется при:
        - Логине адвоката

        Args:
            subject: Основная информация (обычно attorney_id как строка)
            expires_delta: Время жизни (default: 15 минут)
            additional_claims: Доп. данные в токен (email, name и т.д.)

        Returns:
            JWT токен в виде строки

        Example:
            token = SecurityService.create_access_token(
                subject='123',  # attorney_id
                additional_claims={'email': 'attorney@example.com'}
            )
            # Результат: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        '''

        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

        expire = datetime.now(timezone.utc) + expires_delta

        payload = {
            'sub': subject,  # attorney_id
            'exp': expire,  # Время истечения
            'iat': datetime.now(timezone.utc),  # Время создания
            'type': 'access',  # Тип токена
        }

        if additional_claims:
            payload.update(additional_claims)

        encoded_token = jwt.encode(
            payload, settings.secret_key, algorithm=settings.algorithm
        )

        logger.debug(f'Created access token for subject: {subject}')
        return encoded_token

    @staticmethod
    def create_refresh_token(subject: str) -> str:
        '''
        Создать REFRESH TOKEN (долгоживущий, для получения новых access tokens).

        Используется при:
        - Логине адвоката (вместе с access token)
        - Обновлении access token'а (когда истёк)

        Args:
            subject: attorney_id как строка

        Returns:
            JWT токен в виде строки

        Example:
            refresh = SecurityService.create_refresh_token('123')
            # Этот токен живет 7 дней, не требует повторного логина
        '''

        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )

        payload = {
            'sub': subject,
            'exp': expire,
            'iat': datetime.now(timezone.utc),
            'type': 'refresh',  # ← Отличие от access token!
        }

        encoded_token = jwt.encode(
            payload, settings.secret_key, algorithm=settings.algorithm
        )

        logger.debug(f'Created refresh token for subject: {subject}')
        return encoded_token

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            logger.debug(
                f'Token decoded successfully for subject: {payload.get('sub')}'
            )
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning('Token has expired')
            raise ValueError('Token has expired')

        except jwt.InvalidTokenError as e:
            logger.warning(f'Invalid token: {str(e)}')
            raise ValueError(f'Invalid token: {e}')

    @staticmethod
    def verify_token_type(payload: Dict[str, Any], expected_type: str) -> bool:
        '''
        Проверить тип токена (access vs refresh).

        Используется при:
        - Верификации что это именно access token, не refresh

        Args:
            payload: Декодированный payload
            expected_type: 'access' или 'refresh'

        Returns:
            True если тип совпадает

        Example:
            if SecurityService.verify_token_type(payload, 'access'):
                print('Это access token')
            else:
                print('Это refresh token или неправильно')
        '''
        return payload.get('type') == expected_type
