from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subscription:
    id: int
    attorney_id: int
    status: bool
    period_start: datetime
    period_end: datetime
