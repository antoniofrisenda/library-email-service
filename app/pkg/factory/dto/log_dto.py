from dataclasses import dataclass
from typing import Optional


@dataclass
class Log:
    id: str
    outcome: str
    error_msg: Optional[str]
    created_at: str
    email_id: str
