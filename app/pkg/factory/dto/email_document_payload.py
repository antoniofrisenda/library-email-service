import json
from typing import Any, Optional

from pydantic import BaseModel, field_validator


class EmailDTO(BaseModel):
    Type: str
    To: str
    Subject: str = ""
    Body: Optional[dict[str, Any]] = None

    @field_validator("Body", mode="before")
    @classmethod
    def _parse_body(cls, value: Any) -> dict[str, Any] | None:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            parsed: Any = stripped
            for _ in range(4):
                if not isinstance(parsed, str):
                    break
                parsed = json.loads(parsed)
            if isinstance(parsed, dict):
                return parsed
            if isinstance(parsed, list):
                return {"Elementi": parsed}
            return {"Valore": parsed}
        if isinstance(value, dict):
            return value
        return {"Valore": value}
