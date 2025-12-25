from backend.domain.entities.case import Case
from backend.infrastructure.models import CaseORM


class CaseMapper:
    @staticmethod
    def to_domain(orm: CaseORM) -> 'Case':
        '''Конвертация ORM модели Дела в доменную сущность.'''
        return Case(
            id=orm.id,
            name=orm.name,
            client_id=orm.client_id,
            attorney_id=orm.attorney_id,
            status=orm.status,
            description=orm.description,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(domain: 'Case') -> CaseORM:
        '''Конвертация доменной сущности Дела в ORM модель.'''
        return CaseORM(
            id=domain.id,
            name=domain.name,
            client_id=domain.client_id,
            attorney_id=domain.attorney_id,
            status=domain.status,
            description=domain.description,
        )

    @staticmethod
    def update_orm(orm: CaseORM, domain: 'Case') -> None:
        '''
        Обновляет существующий ORM объект значениями из доменной сущности.
        Не обновляет id, created_at, updated_at, attorney_id (они управляются отдельно).
        '''
        orm.name = domain.name
        orm.client_id = domain.client_id
        orm.status = domain.status
        orm.description = domain.description
