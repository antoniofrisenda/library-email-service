from bson import ObjectId
from datetime import datetime
from app.pkg.factory import LogDTO
from app.pkg.domain import LogModel, EmailOutcomeEnum


def log_to_dto(log: LogModel) -> LogDTO:
    return LogDTO(
        outcome=log.outcome.value,
        error_msg=log.error_msg,
        email_id=str(log.email_id)
    )


def dto_to_log(dto: LogDTO) -> LogModel:
    return LogModel(
        outcome=EmailOutcomeEnum(dto.outcome),
        error_msg=dto.error_msg,
        email_id=ObjectId(dto.email_id)
    )
