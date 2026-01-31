from enum import Enum
from typing import Optional
from bson import ObjectId
from dataclasses import dataclass, field
from datetime import datetime, timezone


class EmailOutcomeEnum(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"

@dataclass
class Log:
    email_id: ObjectId
    outcome: EmailOutcomeEnum
    error_msg: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _id: ObjectId = field(default_factory=ObjectId)
