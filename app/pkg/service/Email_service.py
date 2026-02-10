import json
from io import BytesIO
from app.pkg.config import Mailer
from app.pkg.domain import Log, Outcome
from app.pkg.repository import email_repo, log_repo
from app.pkg.factory import email_dto, log_dto, log_dto_map, email_model_map


class MailerService:
    def __init__(self, repo1: email_repo, repo2: log_repo):
        self.email_repo = repo1
        self.log_repo = repo2

    def _send_email(self, payload: email_dto, file_name: str | None = None, file_bytes: BytesIO | None = None) -> log_dto:
        model = self.email_repo.insert(email_model_map(payload))
        log = None

        try:
            Mailer(
                to=payload.To,
                subject=payload.Subject,
                body=json.dumps(payload.Body or {}, ensure_ascii=False),
                file_name=file_name,
                file_bytes=file_bytes
            )
            log = Log(Email_id=model._id, Outcome=Outcome.SENT)

        except Exception as exc:
            log = Log(
                Email_id=model._id,
                Outcome=Outcome.FAILED,
                Error=str(exc)
            )
            raise

        return log_dto_map(self.log_repo.insert(log))

    def mailto(self, payload: email_dto) -> log_dto:
        return self._send_email(payload)

    def mailto_with_attachments(self, payload: email_dto, file_name: str, file_bytes: BytesIO) -> log_dto:
        return self._send_email(payload, file_name=file_name, file_bytes=file_bytes)

    def consume_sqs_msg(self, msg: dict) -> log_dto:
        return self.mailto(email_dto(
            Type=msg["Type"],
            To=msg["To"],
            Subject=msg["Subject"],
            Body=msg.get("Body", {})
        ))
