from dataclasses import dataclass
from typing import Optional


@dataclass
class Log:
    email_id: str
    outcome: str
    error_msg: Optional[str]
