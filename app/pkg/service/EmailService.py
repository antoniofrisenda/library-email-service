import json
from app.pkg.config import send
from app.pkg.domain import LogModel, EmailOutcomeEnum
from app.pkg.repository import EmailRepository, LogRepository
from app.pkg.factory import EmailDTO, LogDTO, dto_to_email, log_to_dto


class EmailService:
    def __init__(self, email_repo: EmailRepository, log_repo: LogRepository):
        self.email_repo = email_repo
        self.log_repo = log_repo

    def send_email(self, payload: EmailDTO) -> LogDTO:
        model = self.email_repo.insert(dto_to_email(payload))

        try:
            send(
                to=payload.address_to,
                body=json.dumps(payload.body_fields or {}, ensure_ascii=False),
            )
            log = LogModel(email_id=model._id, outcome=EmailOutcomeEnum.SENT)

        except Exception as exc:
            log = LogModel(email_id=model._id, outcome=EmailOutcomeEnum.FAILED, error_msg=str(exc))
            raise
        
        return log_to_dto(self.log_repo.insert(log))