from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class EmailDTO:
    type: str
    to: str
    body: Optional[Dict] = None

