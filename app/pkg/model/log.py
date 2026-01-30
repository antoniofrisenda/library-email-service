from enum import Enum
from bson import ObjectId
from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator

PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(lambda v: ObjectId(v) if isinstance(v, str) else v),
]

class EmailOutcomeEnum(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"


class LogCreate(BaseModel):
    email_id: PyObjectId
    outcome: EmailOutcomeEnum
    error_msg: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LogRead(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email_id: PyObjectId
    outcome: EmailOutcomeEnum
    error_msg: str | None
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )