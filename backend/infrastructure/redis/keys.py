class RedisKeys:
    '''Централизованное управление ключами Redis'''

    # Sessions
    @staticmethod
    def session(token_id: str) -> str:
        return f'session:{token_id}'

    # Refresh tokens
    @staticmethod
    def refresh_token(attorney_id: int) -> str:
        return f'refresh_token:attorney:{attorney_id}'

    # Blacklist для revoked токенов
    @staticmethod
    def token_blacklist(token: str) -> str:
        return f'token_blacklist:{token}'

    # Rate limiting
    @staticmethod
    def login_attempts(email: str) -> str:
        return f'login_attempts:{email}'

    @staticmethod
    def login_lockout(email: str) -> str:
        return f'login_lockout:{email}'

    # User cache
    @staticmethod
    def attorney_cache(attorney_id: int) -> str:
        return f'attorney:{attorney_id}'

    # Email verification
    @staticmethod
    def email_verification_code(email: str) -> str:
        return f'email_verification:{email}'

    # Password reset
    @staticmethod
    def password_reset_code(email: str) -> str:
        return f'password_reset:{email}'
