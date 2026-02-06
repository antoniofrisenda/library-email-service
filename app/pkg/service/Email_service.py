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

    def mailto(self, payload: EmailDTO) -> LogDTO:
        model = self.email_repo.insert(email_model(payload))
        register = None

        try:
            mailer(
                to=payload.To,
                subject=payload.Subject,
                body=json.dumps(payload.Body or {}, ensure_ascii=False),
            )
            register = LogModel(Email_id=model._id, Outcome=Outcome.SENT)

        except Exception as exc:
            register = LogModel(
                Email_id=model._id,
                Outcome=Outcome.FAILED,
                Error=str(exc)
            )
            raise

        return log_dto(self.log_repo.insert(register))

    def consume_message(self, msg: dict) -> LogDTO:
        return self.mailto(EmailDTO(
            Type=msg["Type"],
            To=msg["To"],
            Subject=msg["Subject"],
            Body=msg.get("Body", {})
        ))
