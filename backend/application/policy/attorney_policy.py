from backend.application.interfaces.repositories.attorney_repo import (
    IAttorneyRepository,
)

from backend.application.commands.attorney import (
    RegisterAttorneyCommand,
    UpdateAttorneyCommand,
)

from backend.core.exceptions import ValidationException, EntityNotFoundException
from backend.core.logger import logger


class AttorneyPolicy:
    '''Бизнес-логика и правила валидации для Attorney'''

    def __init__(self, repo: IAttorneyRepository):
        self.repo = repo

    async def on_register(self, cmd: RegisterAttorneyCommand) -> None:
        '''
        Валидация при регистрации:
        - Email не должен быть занят
        - License ID должен быть уникален
        - Phone не должен быть занят
        - Пароль соответствует требованиям
        '''

        # 1. Проверить уникальность email
        existing = await self.repo.get_by_email(cmd.email)
        if existing:
            logger.info(f'Email {cmd.email} уже занят')
            raise ValidationException(f'Email {cmd.email} уже зарегистрирован')

        # 2. Проверить уникальность license_id
        existing = await self.repo.get_by_license_id(cmd.license_id)
        if existing:
            logger.info(f'Номер Удостоверения адвоката {cmd.license_id} уже занят')
            raise ValidationException(
                f'Номер Удостоверения адвоката {cmd.license_id} уже зарегистрирован'
            )

        # 3. Проверить уникальность phone
        existing = await self.repo.get_by_phone(cmd.phone)
        if existing:
            logger.info(f'Номер телефона {cmd.phone} уже занят')
            raise ValidationException(f'Номер телефона {cmd.phone} уже занят')

        # 4. Валидировать пароль
        self._validate_password(cmd.password)

        # 5. Валидировать email формат
        self._validate_email(cmd.email)

    async def on_update(self, attorney_id: int, cmd: UpdateAttorneyCommand) -> None:
        '''
        Валидация при обновлении:
        - Юрист существует
        - Новый license_id (если изменяется) не занят
        '''
        # 1. Проверить существование юриста
        attorney = await self.repo.get(attorney_id)
        if not attorney:
            raise EntityNotFoundException(f'Адвокат с ID {attorney_id} не найден')

        # 2. Если изменяется license_id - проверить уникальность
        if cmd.license_id and cmd.license_id != attorney.license_id:
            existing = await self.repo.get_by_license_id(cmd.license_id)
            if existing:
                raise ValidationException(
                    f'Номер Удостоверения адвоката {cmd.license_id} уже занят'
                )

    async def on_delete(self, attorney_id: int) -> None:
        '''Валидация при удалении'''
        attorney = await self.repo.get(attorney_id)
        if not attorney:
            raise EntityNotFoundException(f'Адвокат с ID {attorney_id} не найден')

    @staticmethod
    def _validate_password(password: str) -> None:
        '''Проверить требования к паролю'''
        if len(password) < 8:
            raise ValidationException('Пароль должен содержать минимум 8 символов')
        if not any(c.isdigit() for c in password):
            raise ValidationException('Пароль должен содержать минимум одну цифру')
        if not any(c.isalpha() for c in password):
            raise ValidationException('Пароль должен содержать минимум одну букву')

    @staticmethod
    def _validate_email(email: str) -> None:
        '''Проверить формат email'''
        if '@' not in email or '.' not in email:
            raise ValidationException('Некорректный формат email')
