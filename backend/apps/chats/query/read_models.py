from dataclasses import dataclass
from datetime import datetime


@dataclass
class MessageDTO:
    sender: str
    content: str
    created_at: datetime