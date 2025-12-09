from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from backend.domain.entities.auxiliary import CaseStatus


# ====== COMMANDS (write операции) ======


@dataclass
class CreateCaseCommand:
    name: str
    client_id: int
    attorney_id: int  # из JWT
    description: str
    status: CaseStatus = CaseStatus.NEW  # Дефолтный статус "NEW"


@dataclass
class UpdateCaseCommand:
    client_id: int
    attorney_id: int  # из JWT

    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@dataclass
class DeleteCaseCommand:
    case_id: int


@dataclass
class GetCaseByIdQuery:
    case_id: int


@dataclass
class GetCasesForAttorneyQuery:
    attorney_id: int
    # если потом добавить пагинацию/фильтры:
    # page: int = 1
    # page_size: int = 20
