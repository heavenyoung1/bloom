from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    id: int
    subscription_id: int
    value: int
