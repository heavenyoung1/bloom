from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.application.commands.case import UpdateCaseCommand
from backend.domain.entities.auxiliary import CaseStatus


@dataclass
class Case:
    id: int
    name: str
    client_id: int
    attorney_id: int
    description: str
    status: CaseStatus  # По умолчанию будет CaseStatus.NEW

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        name: str,
        client_id: int,
        attorney_id: int,
        description: str,
        status: CaseStatus = CaseStatus.NEW,
    ) -> 'Case':
        '''Фабричный метод для создания нового дела.'''
        return Case(
            id=None,  # ID будет присвоен после сохранения в базе данных
            name=name,
            client_id=client_id,
            attorney_id=attorney_id,
            description=description,
            status=status,
        )

    def update(self, cmd: UpdateCaseCommand) -> None:
        '''Обновить поля на основе команды, если они не None'''
        if cmd.name is not None:
            self.name = cmd.name
        if cmd.status is not None:
            self.status = cmd.status
        if cmd.description is not None:
            self.description = cmd.description
        if cmd.client_id is not None:
            self.client_id = cmd.client_id
