from enum import Enum
from bson import ObjectId
from dataclasses import dataclass, field
from datetime import datetime, timezone


class EmailTypeEnum(str, Enum):
    RESERVE = "RESERVE"
    RETURN = "RETURN"


@dataclass
class Email:
    email_type: EmailTypeEnum
    address_to: str
    body_fields: dict | None = None
    sent_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
    _id: ObjectId = field(default_factory=ObjectId)
