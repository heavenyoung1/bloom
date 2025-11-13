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
        password_hash: str,
    ) -> Attorney:
        return Attorney(
            id=None,
            license_id=license_id,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            email=email,
            phone=phone,
            password_hash=password_hash,
            is_active=True,
        )
