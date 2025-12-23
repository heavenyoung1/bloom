from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# ====== COMMANDS (write операции) ======

@dataclass
class CreatePaymentDetailtCommand:
    '''Команда на создание платежных реквизитов юриста.'''
    attorney_id: int
    inn: str
    index_address: str
    address: str
    bank_account: str
    correspondent_account: str
    bik: str
    bank_recipient: str
    kpp: Optional[str]  = None


@dataclass
class UpdatePaymentDetailCommand:
    '''Команда на обновление платежных реквизитов.'''
    payment_detail_id: int  # что обновляем (ID записи реквизитов)
    attorney_id: int

    inn: Optional[str] = None
    kpp: Optional[str] = None

    index_address: Optional[str] = None
    address: Optional[str] = None

    bank_account: Optional[str] = None
    correspondent_account: Optional[str] = None
    bik: Optional[str] = None
    bank_recipient: Optional[str] = None

@dataclass
class DeletePaymentDetailCommand:
    '''Команда на удаление платежных реквизитов.'''
    payment_detail_id: int

@dataclass
class GetPaymentDelatilByIdQuery:
    '''Команда на получение платежных реквизитов.'''
    payment_detail_id: int

@dataclass
class GetPaymentDetailForAttorneyQuery:
    '''Команда на получение платежных реквизитов для юриста.'''
    attorney_id: int