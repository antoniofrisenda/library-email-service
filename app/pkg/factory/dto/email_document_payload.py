from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class EmailDTO:
    Type: str
    To: str
    Subject: str
    Body: Optional[Dict] = None
