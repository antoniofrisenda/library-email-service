import json
import logging
from io import BytesIO
from app.pkg.domain import Type
from app.pkg.config import Mailer
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
        model = self.repository.insert(email_model(payload))

        logger.info(
            f"Email saved | "
            f"email_id={getattr(model, '_id', None)} "
            f"to={payload.To} "
            f"subject={payload.Subject}"
        )

        try:
            self.server.send_email_msg(
                to=payload.To,
                subject=payload.Subject,
                body=json.dumps(payload.Body or {}, ensure_ascii=False),
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

    def consume_sqs_msg(self, msg: dict) -> None:
        reservation = msg.get("reservation", {})

        logger.info(f"Processing SQS message | " f"msg={msg} ")

        self.mailto(Dto(
            Type=Type.RESERVE.value,
            To=str(msg.get("user_email")),
            Subject=f"Reservation confirmed for book {reservation.get('book_id')}",
            Body=reservation,
        ))
