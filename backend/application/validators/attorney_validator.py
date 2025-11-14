from backend.infrastructure.repositories.interfaces.attorney_repo import (
    IAttorneyRepository,
)
from backend.application.dto.attorney import CreateAttorneyDTO
from backend.core.exceptions import ValidationException
from backend.core.logger import logger


class AttorneyValidator:
    def __init__(self, repo: IAttorneyRepository):
        self.repo = repo

    async def validate_on_create(self, dto: CreateAttorneyDTO) -> None:
        '''Валидировать данные при создании юриста'''
        attorney_email = await self.repo.get_by_email(dto.email)
        if attorney_email:
            logger(f'Email {dto.email} уже занят')
            raise ValidationException(f'Email {dto.email} уже занят')

        attorney_license = await self.repo.get_by_license_id(dto.license_id)
        if attorney_license:
            logger(f'Номер Удостоверения адвоката {dto.license_id} уже занят')
            raise ValidationException(
                f'Номер Удостоверения адвоката {dto.license_id} уже занят'
            )

        attorney_phone = await self.repo.get_by_phone(dto.phone)
        if attorney_phone:
            logger(f'Номер телефона {dto.phone} уже занят')
            raise ValidationException(f'Номер телефона {dto.phone} уже занят')
