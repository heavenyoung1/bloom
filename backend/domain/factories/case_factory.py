from backend.domain.entities.case import Case
from backend.infrastructure.models.case import CaseStatus


class CaseFactory:
    '''Фабрика для создания Case'''

    @staticmethod
    def create(
        *,
        name: str,
        client_id: int,
        attorney_id: int,
        status: CaseStatus | str,
        description: str | None = None,
    ) -> Case:
        '''Создать новый объект Case'''
        return Case(
            id=None,
            name=name,
            client_id=client_id,
            attorney_id=attorney_id,
            status=status,
            description=description,
        )
