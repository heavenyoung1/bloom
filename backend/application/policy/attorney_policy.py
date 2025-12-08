from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.dto.attorney import RegisterRequest
from backend.core.exceptions import ValidationException
from backend.core.logger import logger


class AttorneyPolicy:
    def __init__(self, repo: IAttorneyRepository):
        self.repo = repo

    async def on_create(self, dto: RegisterRequest) -> None:
        '''Валидировать данные при регистрации'''
        attorney_email = await self.repo.get_by_email(dto.email)
        if attorney_email:
            logger.info(f'Email {dto.email} уже занят')
            raise ValidationException(f'Email {dto.email} уже занят')

        attorney_license = await self.repo.get_by_license_id(dto.license_id)
        if attorney_license:
            logger.info(f'Номер Удостоверения адвоката {dto.license_id} уже занят')
            raise ValidationException(
                f'Номер Удостоверения адвоката {dto.license_id} уже занят'
            )

        attorney_phone = await self.repo.get_by_phone(dto.phone)
        if attorney_phone:
            logger.info(f'Номер телефона {dto.phone} уже занят')
            raise ValidationException(f'Номер телефона {dto.phone} уже занят')
