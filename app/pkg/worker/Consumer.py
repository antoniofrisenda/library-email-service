from app.pkg.api import instance
from app.pkg.config import receive
from app.pkg.factory import EmailDTO
from app.pkg.domain import EmailTypeEnum

def consume(msg: dict | None = None):
    msg = msg or receive()
    while msg:
        try:
            instance().send_email(EmailDTO(
                email_type=EmailTypeEnum(msg["email_type"]),
                address_to=msg["address_to"],
                body_fields=msg.get("body_fields", {})
            ))
        except Exception as e:
            raise e
        finally:
            msg = receive()
