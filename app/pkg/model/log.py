from enum import Enum
from uuid import UUID, uuid4
from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class EmailOutcomeEnum(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"
    
class LogCreate(BaseModel):
    email_id: UUID
    outcome: EmailOutcomeEnum
    error_msg: str | None = None


class LogRead(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id") 
    email_id: UUID
    outcome: EmailOutcomeEnum
    error_msg: str | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
