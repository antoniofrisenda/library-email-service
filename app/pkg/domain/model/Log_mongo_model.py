from enum import Enum
from bson import ObjectId
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field


class EmailOutcome(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"


@dataclass
class LogModel:
    email_id: ObjectId
    outcome: EmailOutcome
    error: Optional[str] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
    _id: ObjectId = field(default_factory=ObjectId)
