from enum import Enum
from uuid import UUID, uuid4
from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class EmailTypeEnum(str, Enum):
    RESERVE = "RESERVE"
    RETURN = "RETURN"

class EmailCreate(BaseModel):
    email_type: EmailTypeEnum
    address_to: str
    body_fields: dict | None = None


class EmailRead(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id") 
    email_type: EmailTypeEnum
    address_to: str
    body_fields: dict
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
