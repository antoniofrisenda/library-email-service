from typing import Optional
from dataclasses import dataclass


@dataclass
class LogDTO:
    Email_id: str
    Outcome: str
    Error: Optional[str] = None
