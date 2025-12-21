from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import bcrypt
import jwt
from backend.core.settings import settings
from backend.core.logger import logger


class SecurityService:
    '''Сервис для работы с паролями и JWT токенами'''

    # ========== PASSWORD ==========

    @staticmethod
    def hash_password(password: str) -> str:
        '''Захешировать пароль (bcrypt)'''
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        '''Проверить пароль'''
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    # ========== JWT TOKEN ==========

    @staticmethod
    def create_access_token(
        subject: str,
        expires_delta: Optional[timedelta] = None,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        '''
        Создать ACCESS TOKEN (короткоживущий, для API запросов).

        Используется при:
        - Логине адвоката (вместе с refresh token)

        Args:
            subject: attorney_id как строка
            expires_delta: Время жизни (default: settings.access_token_expire_minutes)
            additional_claims: Дополнительные claims (email, name и т.д.)

        Returns:
            JWT токен в виде строки
        '''

        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

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
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        logger.debug(f'Access token создан для: {subject}')
        return encoded_token

    @staticmethod
    def create_refresh_token(subject: str) -> str:
        '''
        Создать REFRESH TOKEN (долгоживущий, для получения новых access tokens).

        Используется при:
        - Логине адвоката (вместе с access token)

        Args:
            subject: attorney_id как строка

        Returns:
            JWT токен в виде строки
        '''
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        payload = {
            'sub': subject,
            'exp': expire,
            'iat': datetime.now(timezone.utc),
            'type': 'refresh',  # Отличие от access token!
        }

        encoded_token = jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        logger.debug(f'Refresh token создан для: {subject}')
        return encoded_token

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        '''
        Декодировать JWT токен.

        Args:
            token: JWT токен в виде строки

        Returns:
            Декодированный payload

        Raises:
            ValueError: Если токен истёк или невалиден
        '''
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            logger.debug(f'Token декодирован для: {payload.get('sub')}')
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning('Token истёк')
            raise ValueError('Token истёк')

        except jwt.InvalidTokenError as e:
            logger.warning(f'Невалидный token: {str(e)}')
            raise ValueError(f'Невалидный token: {e}')

    @staticmethod
    def verify_token_type(payload: Dict[str, Any], expected_type: str) -> bool:
        '''
        Проверить тип токена (access vs refresh).

        Args:
            payload: Декодированный payload
            expected_type: 'access' или 'refresh'

        Returns:
            True если тип совпадает, иначе False
        '''
        return payload.get('type') == expected_type

    @staticmethod
    def get_subject_from_token(payload: Dict[str, Any]) -> str:
        '''
        Получить attorney_id из декодированного токена.

        Args:
            payload: Декодированный payload

        Returns:
            attorney_id как строка

        Raises:
            ValueError: Если subject отсутствует в payload
        '''
        subject = payload.get('sub')
        if not subject:
            raise ValueError('Subject отсутствует в token payload')
        return subject
