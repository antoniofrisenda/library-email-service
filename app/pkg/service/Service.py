import json
from app.pkg.config import mailer
from app.pkg.domain import LogModel, Outcome
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
                to=payload.to,
                body=json.dumps(payload.body or {}, ensure_ascii=False),
            )
            register = LogModel(email_id=model._id, outcome=Outcome.SENT)

        except Exception as exc:
            register = LogModel(
                email_id=model._id,
                outcome=Outcome.FAILED,
                error=str(exc)
            )
            raise

        return log_dto(self.log_repo.insert(register))
