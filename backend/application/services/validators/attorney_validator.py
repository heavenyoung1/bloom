from backend.infrastructure.repositories.interfaces.attorney_repo import IAttorneyRepository
from backend.application.dto.attorney import CreateAttorneyDTO

class AttorneyValidator:
    def __init__(self, repo: IAttorneyRepository):
        self.repo = repo

    async def validate_on_create(self, dto: CreateAttorneyDTO) -> None:
        