from app.pkg.api import instance
from app.pkg.config import receiver
from app.pkg.factory import EmailDTO


def consume_queue(msg: dict | None = None):
    msg = msg or receiver()
    while msg:
        try:
            instance().mailto(
                EmailDTO(
                    type=msg["type"],
                    to=msg["to"],
                    body=msg.get("body", {})
                )
            )
        finally:
            msg = receiver()
