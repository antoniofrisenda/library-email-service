from typing import Optional
from dataclasses import dataclass


@dataclass
class LogDTO:
    email_id: str
    outcome: str
    error: Optional[str] = None
