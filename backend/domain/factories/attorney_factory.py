from backend.domain.entities.attorney import Attorney


class AttorneyFactory:
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
    ) -> Attorney:
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
        )
