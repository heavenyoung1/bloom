from backend.domain.entities.attorney import Attorney
from backend.infrastructure.models import AttorneyORM


class AttorneyMapper:
    @staticmethod
    def to_domain(orm: 'AttorneyORM') -> 'Attorney':
        '''Конвертация ORM модели в сущность домена.'''
        return Attorney(
            id=orm.id,
            license_id=orm.license_id,
            first_name=orm.first_name,
            last_name=orm.last_name,
            patronymic=orm.patronymic,
            email=orm.email,
            phone=orm.phone,
            password_hash=orm.password_hash,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(domain: 'Attorney') -> 'AttorneyORM':
        '''Конвертация сущности домена в ORM модель.'''
        return AttorneyORM(
            id=domain.id,
            license_id=domain.license_id,
            first_name=domain.first_name,
            last_name=domain.last_name,
            patronymic=domain.patronymic,
            email=domain.email,
            phone=domain.phone,
            password_hash=domain.password_hash,
            is_active=domain.is_active,
        )
