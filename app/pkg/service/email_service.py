import json
from io import BytesIO
from loguru import logger
from app.pkg.config import Mailer
from app.pkg.repository import Repo
from app.pkg.factory import Dto, email_model


class MailerService:
    def __init__(self, repository: Repo):
        self.repository = repository
        self.server = Mailer()

    def _send_email(self, payload: Dto, file_name: str | None = None, file_bytes: BytesIO | None = None,) -> None:

        model = self.repository.insert(email_model(payload))

        logger.bind(email_id=getattr(model, "_id", None),
                    to=payload.To,
                    subject=payload.Subject,
                ).info("Email saved")

        try:
            self.server.send_email_msg(
                to=payload.To,
                subject=payload.Subject,
                body=json.dumps(payload.Body or {}, ensure_ascii=False),
                file_name=file_name,
                file_bytes=file_bytes,
            )

            logger.bind(email_id=getattr(model, "_id", None),
                        to=payload.To,
                        subject=payload.Subject,
                    ).info("Email sent")

        except Exception:
            logger.bind(email_id=getattr(model, "_id", None),
                        to=payload.To,
                        subject=payload.Subject,
                    ).warning("Email sending failed")
            raise

    def mailto(self, payload: Dto) -> None:
        self._send_email(payload)

    def mailto_with_attachments(self, payload: Dto, file_name: str, file_bytes: BytesIO,) -> None:
        self._send_email(payload, file_name=file_name, file_bytes=file_bytes)

    def consume_sqs_msg(self, msg: dict) -> None:
        self.mailto(Dto(
            Type=msg["Type"],
            To=msg["To"],
            Subject=msg["Subject"],
            Body=msg.get("Body", {}),
        )
    )
