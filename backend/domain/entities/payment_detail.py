from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# from backend.application.dto.details_payment import (
#     pass
# )

@dataclass
class PaymentDetail:
    id: int                     # ID платежной информации, генерируется автоматически
    attorney_id: int            # Владелец платежа - юрист

    inn: str                    # ИНН получателя
    kpp: Optional[str]          # КПП

    index_address: str          # Индекс адреса
    address: str                # Адрес 

    bank_account: str           # Номер расчетного счета
    correspondent_account: str  # Корреспондентский счет
    bik: str                    # БИК
    bank_recipient: str         # Банк-получатель

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        attorney_id: int,
        inn: str,
        kpp: Optional[str],
        index_address: str,
        address: str,
        bank_account: str,
        correspondent_account: str,
        bik: str,
        bank_recipient: str,
        taxable: bool,
        condition: Optional[str] = None,
    ) -> 'PaymentDetail':
        '''Фабричный метод для создания платежных реквизитов.'''
        return PaymentDetail(
            id=None,
            attorney_id=attorney_id,
            inn=inn,
            kpp=kpp,
            index_address=index_address,
            address=address,
            bank_account=bank_account,
            correspondent_account=correspondent_account,
            bik=bik,
            bank_recipient=bank_recipient,
            taxable=taxable,
            condition=condition,
        )

    def update(self, cmd: UpdatePaymentDetailCommand) -> None:
        '''Обновить поля на основе команды, если они не None.'''
        if cmd.inn is not None:
            self.inn = cmd.inn
        if cmd.kpp is not None:
            self.kpp = cmd.kpp
        if cmd.index_address is not None:
            self.index_address = cmd.index_address
        if cmd.address is not None:
            self.address = cmd.address
        if cmd.bank_account is not None:
            self.bank_account = cmd.bank_account
        if cmd.correspondent_account is not None:
            self.correspondent_account = cmd.correspondent_account
        if cmd.bik is not None:
            self.bik = cmd.bik
        if cmd.bank_recipient is not None:
            self.bank_recipient = cmd.bank_recipient
        if cmd.taxable is not None:
            self.taxable = cmd.taxable
        if cmd.condition is not None:
            self.condition = cmd.condition
