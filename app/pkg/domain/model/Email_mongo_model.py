from enum import Enum
from bson import ObjectId
from datetime import datetime, timezone
from dataclasses import dataclass, field


class EmailType(str, Enum):
    RESERVE = "RESERVE"
    RETURN = "RETURN"


@dataclass
class EmailModel:
    type: EmailType
    to: str
    body: dict | None = None
    sent_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
    _id: ObjectId = field(default_factory=ObjectId)
