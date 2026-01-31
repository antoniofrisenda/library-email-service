from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Email:
    id: str
    email_type: str
    address_to: str
    body_fields: Optional[Dict]
    sent_at: str
