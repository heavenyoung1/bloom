from backend.domain.entities.client import Client
from backend.infrastructure.models import ClientORM


class ClientMapper:
    @staticmethod
    def to_domain(orm: ClientORM) -> 'Client':
        '''Конвертация ORM модели клиента в доменную сущность.'''
        return Client(
            id=orm.id,
            name=orm.name,
            type=orm.type,
            email=orm.email,
            phone=orm.phone,
            personal_info=orm.personal_info,
            address=orm.address,
            messenger=orm.messenger,
            messenger_handle=orm.messenger_handle,
            created_at=orm.created_at,
            owner_attorney_id=orm.owner_attorney_id,
        )

    @staticmethod
    def to_orm(domain: 'Client') -> ClientORM:
        '''Конвертация доменной сущности клиента в ORM модель.'''
        return ClientORM(
            id=domain.id,
            name=domain.name,
            type=domain.type,
            email=domain.email,
            phone=domain.phone,
            personal_info=domain.personal_info,
            address=domain.address,
            messenger=domain.messenger,
            messenger_handle=domain.messenger_handle,
            created_at=domain.created_at,
            owner_attorney_id=domain.owner_attorney_id,
        )
