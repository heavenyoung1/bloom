from backend.domain.entities.contact import Contact
from backend.infrastructure.models import ContactORM


class ContactMapper:
    @staticmethod
    def to_domain(orm: ContactORM) -> 'Contact':
        '''Конвертация ORM модели контакта в доменную сущность.'''
        return Contact(
            id=orm.id,
            name=orm.name,
            personal_info=orm.personal_info,
            phone=orm.phone,
            email=orm.email,
            created_at=orm.created_at,
            case_id=orm.case_id,
            attorney_id=orm.attorney_id,
        )

    @staticmethod
    def to_orm(domain: 'Contact') -> 'ContactORM':
        '''Конвертация доменной сущности контакта в ORM модель.'''
        return ContactORM(
            id=domain.id,
            name=domain.name,
            personal_info=domain.personal_info,
            phone=domain.phone,
            email=domain.email,
            created_at=domain.created_at,
            case_id=domain.case_id,
            attorney_id=domain.attorney_id,
        )
