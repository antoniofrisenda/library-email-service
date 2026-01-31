from enum import Enum
from bson import ObjectId
from dataclasses import dataclass, field
from datetime import datetime, timezone


class EmailOutcomeEnum(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"


@dataclass
class Log:
    outcome: EmailOutcomeEnum
    error_msg: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
    email_id: ObjectId
    id: ObjectId = field(default_factory=ObjectId, alias="_id")
