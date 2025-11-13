from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository
)
from backend.application.dto.attorney import CreateAttorneyDTO
from backend.core.exceptions import ValidationException
from backend.core.logger import logger


class AttorneyValidator:
    def __init__(self, repo: IAttorneyRepository):
        self.repo = repo

    async def validate_on_create(self, dto: CreateAttorneyDTO) -> None:
        '''Валидировать данные при создании юриста'''
        if await self.repo.get_by_email(dto.email):
            logger(f'Email {dto.email} уже занят')
            raise ValidationException(f'Email {dto.email} уже занят')

        if await self.repo.get_by_license_id(dto.license_id):
            logger(f'Номер Удостоверения адвоката {dto.license_id} уже занят')
            raise ValidationException(
                f'Номер Удостоверения адвоката {dto.license_id} уже занят'
            )

        if await self.repo.get_by_license_id(dto.phone_number):
            logger(f'Номер телефона {dto.phone_number} уже занят')
            raise ValidationException(f'Номер телефона {dto.phone_number} уже занят')
