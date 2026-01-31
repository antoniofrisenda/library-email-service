from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Email:
    email_type: str
    address_to: str
    body_fields: Optional[Dict]
