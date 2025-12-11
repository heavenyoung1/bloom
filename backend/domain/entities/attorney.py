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
    phone: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        license_id: str,
        first_name: str,
        last_name: str,
        patronymic: str | None,
        email: str,
        phone: str | None,
        hashed_password: str,
    ) -> 'Attorney':
        return Attorney(
            id=None,
            license_id=license_id,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            email=email,
            phone=phone,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
