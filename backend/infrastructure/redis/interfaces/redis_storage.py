from abc import ABC, abstractmethod
from typing import Optional, List
from backend.domain.entities.session import RefreshSession
from uuid import UUID


class IRefreshSessionStore(ABC):
    @abstractmethod
    async def save(self, session: RefreshSession) -> None: ...

    @abstractmethod
    async def get(self, jti: str) -> Optional[RefreshSession]: ...

    @abstractmethod
    async def delete(self, jti: str) -> None: ...

    @abstractmethod
    async def delete_all_for_user(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def list_for_user(self, user_id: UUID) -> List[RefreshSession]: ...
