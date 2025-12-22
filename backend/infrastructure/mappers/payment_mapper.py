from backend.domain.entities.payment import ClientPayment
from backend.infrastructure.models import ClientPaymentORM


class ClientPaymentMapper:
    @staticmethod
    def to_domain(orm: ClientPaymentORM) -> 'ClientPayment':
        '''Конвертация ORM модели Платежа в доменную сущность.'''
        return ClientPayment(
            id=orm.id,
            name=orm.name,
            client_id=orm.client_id,
            attorney_id=orm.attorney_id,
            paid=orm.paid,
            paid_str=orm.paid_str,
            pade_date=orm.pade_date,
            paid_deadline=orm.paid_deadline,
            status=orm.status,
            taxable=orm.taxable,
            condition=orm.condition,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(domain: 'ClientPayment') -> ClientPaymentORM:
        '''Конвертация доменной сущности Платежа в ORM модель.'''
        return ClientPaymentORM(
            id=domain.id,
            name=domain.name,
            client_id=domain.client_id,
            attorney_id=domain.attorney_id,
            paid=domain.paid,
            paid_str=domain.paid_str,
            pade_date=domain.pade_date,
            paid_deadline=domain.paid_deadline,
            status=domain.status,
            taxable=domain.taxable,
            condition=domain.condition,
        )