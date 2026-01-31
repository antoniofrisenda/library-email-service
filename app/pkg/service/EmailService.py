import json
from app.pkg.config import send
from app.pkg.domain import EmailOutcomeEnum
from app.pkg.repository import EmailRepository, LogRepository
from app.pkg.factory import EmailDTO, LogDTO, EmailMapper, LogMapper


class EmailService:
    def __init__(self, repo1: EmailRepository, repo2: LogRepository):
        self.email_repo = repo1
        self.log_repo = repo2

    def send_email(self, payload: EmailDTO) -> EmailDTO:
        model = self.email_repo.insert(EmailMapper.dto_to_email(payload))
        log_dto = None

        try:
            send(
                to=payload.address_to,
                body=json.dumps(payload.body_fields or {}, ensure_ascii=False),
            )

            log_dto = LogDTO(email_id=model.id,
                             outcome=EmailOutcomeEnum.SENT.value)
        except Exception as exc:
            log_dto = LogDTO(
                email_id=model.id,
                outcome=EmailOutcomeEnum.FAILED.value,
                error_msg=str(exc),
            )
            raise
        finally:
            if log_dto:
                self.log_repo.insert(LogMapper.dto_to_log(log_dto))

        return EmailMapper.email_to_dto(model)
