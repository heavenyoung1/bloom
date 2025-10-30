from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    id: int
    file_name: str
    storage_path: str
    checksum: str
    client_id: int
    case_id: int
    attorney: int
    created_at: datetime
