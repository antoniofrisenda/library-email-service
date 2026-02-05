from bson import ObjectId
from app.pkg.factory import LogDTO
from app.pkg.domain import LogModel, Outcome


def _to_log_model(dto: LogDTO) -> LogModel:
    return LogModel(
        outcome=Outcome(dto.outcome),
        error=dto.error,
        email_id=ObjectId(dto.email_id)
    )


def _from_log_model(model: LogModel) -> LogDTO:
    return LogDTO(
        outcome=model.outcome.value,
        error=model.error,
        email_id=str(model.email_id)
    )
