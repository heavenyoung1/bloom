from backend.domain.entities.payment_detail import PaymentDetail
from backend.infrastructure.models.payment_detail import PaymentDetailORM


class PaymentDetailMapper:
    @staticmethod
    def to_domain(orm: PaymentDetailORM) -> 'PaymentDetail':
        '''Конвертация ORM модели PaymentDetail в доменную сущность.'''
        return PaymentDetail(
            id=orm.id,
            attorney_id=orm.attorney_id,
            inn=orm.inn,
            kpp=orm.kpp,
            index_address=orm.index_address,
            address=orm.address,
            bank_account=orm.bank_account,
            correspondent_account=orm.correspondent_account,
            bik=orm.bik,
            bank_recipient=orm.bank_recipient,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(domain: 'PaymentDetail') -> PaymentDetailORM:
        '''Конвертация доменной сущности PaymentDetail в ORM модель.'''
        return PaymentDetailORM(
            id=domain.id,
            attorney_id=domain.attorney_id,
            inn=domain.inn,
            kpp=domain.kpp,
            index_address=domain.index_address,
            address=domain.address,
            bank_account=domain.bank_account,
            correspondent_account=domain.correspondent_account,
            bik=domain.bik,
            bank_recipient=domain.bank_recipient,
        )

    @staticmethod
    def update_orm(orm: PaymentDetailORM, domain: 'PaymentDetail') -> None:
        '''
        Обновляет существующий ORM объект значениями из доменной сущности.
        Не обновляет id, created_at, updated_at, attorney_id (они управляются отдельно).
        '''
        orm.inn = domain.inn
        orm.kpp = domain.kpp
        orm.index_address = domain.index_address
        orm.address = domain.address
        orm.bank_account = domain.bank_account
        orm.correspondent_account = domain.correspondent_account
        orm.bik = domain.bik
        orm.bank_recipient = domain.bank_recipient