import json
from app.pkg.config import send
from datetime import datetime, timezone
from app.pkg.repository import EmailRepository, LogRepository
from app.pkg.model import EmailCreate, EmailRead, LogCreate, LogRead, EmailOutcomeEnum


class EmailService:
    def __init__(self, repo1: EmailRepository, repo2: LogRepository):
        self.email_repo = repo1
        self.log_repo = repo2

    def send_email(self, payload: EmailCreate) -> EmailRead:
        model = self.email_repo.insert(EmailRead(
            email_type=payload.email_type,
            address_to=payload.address_to,
            body_fields=payload.body_fields or {},
            sent_at=datetime.now(timezone.utc)
        ))

        log = None

        try:
            send(
                to=payload.address_to,
                body=json.dumps(payload.body_fields or {}, ensure_ascii=False)
            )
            log = LogCreate(
                email_id=model.id,
                outcome=EmailOutcomeEnum.SENT
            )
        except Exception as exc:
            log = LogCreate(
                email_id=model.id,
                outcome=EmailOutcomeEnum.FAILED,
                error_msg=str(exc)
            )
            raise

        self.log_repo.insert(LogRead.model_validate(log.model_dump()))
        return model