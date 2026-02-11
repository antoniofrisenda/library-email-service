import json
import logging
from io import BytesIO
from app.pkg.config import Mailer
from app.pkg.repository import Repo
from app.pkg.factory import Dto, email_model

logger = logging.getLogger(__name__)


class MailerService:
    def __init__(self, repository: Repo):
        self.repository = repository
        self.server = Mailer()

    def _send_email(self, payload: Dto,
                    file_name: str | None = None,
                    file_bytes: BytesIO | None = None
                    ):

        model = self.repository.insert(email_model(payload))

        logger.info("Email saved", extra={
            "email_id": getattr(model, "_id", None),
            "to": payload.To,
            "subject": payload.Subject
        }
        )

        try:
            self.server.send_email_msg(
                to=payload.To,
                subject=payload.Subject,
                body=json.dumps(payload.Body or {}, ensure_ascii=False),
                file_name=file_name,
                file_bytes=file_bytes
            )

            logger.info("Email sent", extra={"email_id": getattr(
                model, "_id", None), "to": payload.To})

        except Exception as exc:
            logger.exception("Email sending failed", extra={
                             "email_id": getattr(model, "_id", None), "to": payload.To})
            raise

    def mailto(self, payload: Dto):
        return self._send_email(payload)

    def mailto_with_attachments(self, payload: Dto, file_name: str, file_bytes: BytesIO):
        return self._send_email(payload, file_name=file_name, file_bytes=file_bytes)

    def consume_sqs_msg(self, msg: dict):
        return self.mailto(Dto(
            Type=msg["Type"],
            To=msg["To"],
            Subject=msg["Subject"],
            Body=msg.get("Body", {})
        ))
