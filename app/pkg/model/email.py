from enum import Enum
from bson import ObjectId
from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator

class EmailTypeEnum(str, Enum):
    RESERVE = "RESERVE"
    RETURN = "RETURN"

PyObjectId = Annotated[ObjectId,
    BeforeValidator(lambda S: ObjectId(S) if isinstance(S, str) else S),
]

class EmailCreate(BaseModel):
    email_type: EmailTypeEnum
    address_to: str
    body_fields: dict | None = None
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EmailRead(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email_type: EmailTypeEnum
    address_to: str
    body_fields: dict | None
    sent_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
