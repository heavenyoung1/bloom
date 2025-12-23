from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.application.commands.attorney import UpdateAttorneyCommand


@dataclass
class Attorney:
    id: int
    license_id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str
    hashed_password: str  # Обязательное поле идёт первым
    is_active: bool
    is_superuser: bool
    is_verified: bool

    phone: Optional[str] = None  # Опциональное поле с дефолтным значением
    telegram_username: Optional[str] = None  # Опциональное поле с дефолтным значением
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        license_id: str,
        first_name: str,
        last_name: str,
        patronymic: Optional[str] = None,
        email: str,
        hashed_password: str,
        phone: Optional[str] = None,
        telegram_username: Optional[str] = None,
    ) -> 'Attorney':
        return Attorney(
            id=None,
            license_id=license_id,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            email=email,
            hashed_password=hashed_password,  # Обязательное поле идёт первым
            is_active=True,
            is_superuser=False,
            is_verified=False,
            phone=phone,  # Опциональные поля идут после обязательных
            telegram_username=telegram_username,
        )

    def update(self, cmd: UpdateAttorneyCommand) -> None:
        '''Обновить поля на основе команды, если они не None (PATCH-семантика)'''
        if cmd.first_name is not None:
            self.first_name = cmd.first_name
        if cmd.last_name is not None:
            self.last_name = cmd.last_name
        if cmd.patronymic is not None:
            self.patronymic = cmd.patronymic
        if cmd.phone is not None:
            self.phone = cmd.phone
        if cmd.license_id is not None:
            self.license_id = cmd.license_id
        if cmd.telegram_username is not None:
            self.telegram_username = cmd.telegram_username
        if cmd.email is not None:
            self.email = cmd.email
