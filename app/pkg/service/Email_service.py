from io import BytesIO
import json
from app.pkg.config import mailer
from app.pkg.domain import LogModel, Outcome
from app.pkg.factory.dto.DTO_log import LogDTO
from app.pkg.repository import email_repo, log_repo
from app.pkg.factory import EmailDTO, LogDTO, email_model, log_dto


class MailerService:
    def __init__(self, repo1: email_repo, repo2: log_repo):
        self.email_repo = repo1
        self.log_repo = repo2

    def _send_email(self, payload: EmailDTO, file_name: str | None = None, file_bytes: BytesIO | None = None) -> LogDTO:
        model = self.email_repo.insert(email_model(payload))
        log = None

        try:
            mailer(
                to=payload.To,
                subject=payload.Subject,
                body=json.dumps(payload.Body or {}, ensure_ascii=False),
                file_name=file_name,
                file_bytes=file_bytes
            )
            log = LogModel(Email_id=model._id, Outcome=Outcome.SENT)

        except Exception as exc:
            log = LogModel(
                Email_id=model._id,
                Outcome=Outcome.FAILED,
                Error=str(exc)
            )
            raise

        return log_dto(self.log_repo.insert(log))

    def mailto(self, payload: EmailDTO) -> LogDTO:
        return self._send_email(payload)

    def mailto_with_attachments(self, payload: EmailDTO, file_name: str, file_bytes: BytesIO) -> LogDTO:
        return self._send_email(payload, file_name=file_name, file_bytes=file_bytes)

    def consume_message(self, msg: dict) -> LogDTO:
        return self.mailto(EmailDTO(
            Type=msg["Type"],
            To=msg["To"],
            Subject=msg["Subject"],
            Body=msg.get("Body", {})
        ))
