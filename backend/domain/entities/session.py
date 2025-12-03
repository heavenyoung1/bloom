from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class RefreshSession:
    jti: str
    user_id: UUID
    user_agent: str | None
    ip: str | None
    expires_at: datetime
    created_at: datetime
