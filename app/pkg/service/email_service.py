import json
import logging
from io import BytesIO
from app.pkg.domain import Type
from app.pkg.config import Mailer
from app.pkg.middleware import (
    extract_body_from_message,
    format_email_body,
    format_email_subject,
    normalize_body,
)
from app.pkg.repository import Repo
from app.pkg.factory import Dto, email_model


logger = logging.getLogger("app")


class MailerService:
    def __init__(self, repository: Repo) -> None:
        try:
            self.repository = repository
            self.server = Mailer()
            logger.info("Service init OK")
        except Exception:
            logger.warning("Service init failed")
            raise

    def _send_email(self, payload: Dto, file_name: str | None = None, file_bytes: BytesIO | None = None) -> None:
        body = normalize_body(payload.Body)
        subject = payload.Subject or format_email_subject(payload.Type, body)
        model = self.repository.insert(email_model(payload))

        logger.info(
            f"Email saved | "
            f"email_id={getattr(model, '_id', None)} "
            f"to={payload.To} "
            f"subject={subject}"
        )

        try:
            plain_body, html_body = format_email_body(payload.Type, body)
            self.server.send_email_msg(
                to=payload.To,
                subject=subject,
                body=plain_body,
                html_body=html_body,
                file_name=file_name,
                file_bytes=file_bytes,
            )

            logger.info(
                f"Email sent | " f"email_id={getattr(model, '_id', None)} ")

        except Exception:
            logger.warning(f"Email sending failed")
            raise

    def mailto(self, payload: Dto) -> None:
        self._send_email(payload)

    def mailto_with_attachments(self, payload: Dto, file_name: str, file_bytes: BytesIO) -> None:
        self._send_email(
            payload,
            file_name=file_name,
            file_bytes=file_bytes,
        )

    def consume_sqs_msg(self, msg: dict | str) -> None:
        parsed: dict = json.loads(msg) if isinstance(msg, str) else msg

        logger.info(f"Processing SQS message | msg={parsed} ")

        email_type = str(parsed.get("Type") or parsed.get("type") or Type.RESERVE.value)
        body = extract_body_from_message(parsed)
        to = parsed.get("To") or parsed.get("to") or parsed.get("user_email")
        subject = parsed.get("Subject") or parsed.get("subject") or format_email_subject(
            email_type, body
        )

        self.mailto(Dto(
            Type=email_type,
            To=str(to),
            Subject=subject,
            Body=body,
        ))
