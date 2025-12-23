from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from backend.domain.entities.auxiliary import PaymentStatus
from backend.application.commands.client_payment import (
    UpdatePaymentCommand,
    ChangePaymentStatusCommand,
)


@dataclass
class ClientPayment:
    id: int
    name: str
    client_id: int
    attorney_id: int
    paid: float
    paid_str: str
    pade_date: date
    paid_deadline: Optional[date]
    status: PaymentStatus
    taxable: bool = False
    condition: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        name: str,
        client_id: int,
        attorney_id: int,
        paid: float,
        paid_str: str,
        pade_date: date,
        paid_deadline: Optional[datetime],
        taxable: bool = False,
        condition: Optional[str] = None,
        status: PaymentStatus = PaymentStatus.issued,
    ) -> 'ClientPayment':
        '''Фабричный метод для создания нового платежа.'''
        return ClientPayment(
        id = None,  # ID будет присвоен после сохранения в базе данных
        name=name,
        client_id=client_id,
        attorney_id=attorney_id,
        paid=paid,
        paid_str=paid_str,
        pade_date=pade_date,
        paid_deadline=paid_deadline,
        taxable=taxable,
        condition=condition,
        status=status,
        )

    def update(self, cmd: UpdatePaymentCommand) -> None:
        '''Обновить поля на основе команды, если они не None'''
        if cmd.name is not None:
            self.name = cmd.name
        if cmd.client_id is not None:
            self.client_id = cmd.client_id
        if cmd.attorney_id is not None:
            self.attorney_id = cmd.attorney_id
        if cmd.paid is not None:
            self.paid = cmd.paid
        if cmd.paid_str is not None:
            self.paid_str = cmd.paid_str
        if cmd.pade_date is not None:
            self.pade_date = cmd.pade_date
        if cmd.taxable is not None:
            self.taxable = cmd.taxable
        if cmd.condition is not None:
            self.condition = cmd.condition
        if cmd.paid_deadline is not None:
            self.paid_deadline = cmd.paid_deadline
        if cmd.status is not None:
            self.status = cmd.status

    def change_status(self, cmd: ChangePaymentStatusCommand) -> None:
        '''Изменить статус платежа'''
        self.status = cmd.status
