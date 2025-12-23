from datetime import datetime, date
from backend.domain.entities.client_payment import ClientPayment
from backend.infrastructure.models import ClientPaymentORM


class ClientPaymentMapper:
    @staticmethod
    def to_domain(orm: ClientPaymentORM) -> 'ClientPayment':
        '''Конвертация ORM модели Платежа в доменную сущность.'''
        # Преобразуем datetime в date для paid_deadline
        paid_deadline_date = None
        if orm.paid_deadline:
            if isinstance(orm.paid_deadline, datetime):
                paid_deadline_date = orm.paid_deadline.date()
            elif isinstance(orm.paid_deadline, date):
                paid_deadline_date = orm.paid_deadline
        
        return ClientPayment(
            id=orm.id,
            name=orm.name,
            client_id=orm.client_id,
            attorney_id=orm.attorney_id,
            paid=orm.paid,
            paid_str=orm.paid_str,
            pade_date=orm.pade_date,
            paid_deadline=paid_deadline_date,
            status=orm.status,
            taxable=orm.taxable,
            condition=orm.condition,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(domain: 'ClientPayment') -> ClientPaymentORM:
        '''Конвертация доменной сущности Платежа в ORM модель.'''
        # Преобразуем date в datetime для paid_deadline (если нужно)
        paid_deadline_datetime = None
        if domain.paid_deadline:
            if isinstance(domain.paid_deadline, date):
                # Преобразуем date в datetime (начало дня)
                paid_deadline_datetime = datetime.combine(domain.paid_deadline, datetime.min.time())
            elif isinstance(domain.paid_deadline, datetime):
                paid_deadline_datetime = domain.paid_deadline
        
        return ClientPaymentORM(
            id=domain.id,
            name=domain.name,
            client_id=domain.client_id,
            attorney_id=domain.attorney_id,
            paid=domain.paid,
            paid_str=domain.paid_str,
            pade_date=domain.pade_date,
            paid_deadline=paid_deadline_datetime,
            status=domain.status,
            taxable=domain.taxable,
            condition=domain.condition,
        )