from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from backend.domain.entities.auxiliary import Messenger

# ====== COMMANDS (write операции) ======


@dataclass
class CreateCaseCommand:
    name: str
    client_id: int
    owner_attorney_id: int  # из JWT
    status: str
    description: str


@dataclass
class UpdateCaseCommand:
    client_id: int
    owner_attorney_id: int  # из JWT

    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


@dataclass
class DeleteCaseCommand:
    case_id: int


@dataclass
class GetCaseByIdQuery:
    case_id: int


@dataclass
class GetCasesForAttorneyQuery:
    owner_attorney_id: int
    # если потом добавить пагинацию/фильтры:
    # page: int = 1
    # page_size: int = 20
