from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClientPayment:
    id: int
    name: str
    sender: str
    paid: int
    paid_str: str
    date: datetime
    status: str

    @staticmethod
    def create():
        pass