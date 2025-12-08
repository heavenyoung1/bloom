from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.application.commands.case import UpdateCaseCommand


@dataclass
class Case:
    id: int
    name: str
    client_id: int
    attorney_id: int
    status: str
    description: str

    # Необязательные атрибуты
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        name: str,
        client_id: int,
        attorney_id: int,
        status: str,
        description: str,
    ) -> 'Case':
        return Case(
            id=None,
            name=name,
            client_id=client_id,
            attorney_id=attorney_id,
            status=status,
            description=description,
        )

    def update(self, cmd: UpdateCaseCommand) -> None:
        '''Обновить поля на основе команды, если они не None'''
        if cmd.name is not None:
            self.name = cmd.name
        if cmd.status is not None:
            self.status = cmd.status
        if cmd.description is not None:
            self.cmd = cmd.description
        if cmd.client_id is not None:
            self.client_id = cmd.client_id
