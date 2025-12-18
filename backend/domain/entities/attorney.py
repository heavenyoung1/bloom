from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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