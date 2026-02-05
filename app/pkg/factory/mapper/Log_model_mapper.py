from bson import ObjectId
from app.pkg.factory import LogDTO
from app.pkg.domain import LogModel, Outcome


def _to_log_model(dto: LogDTO) -> LogModel:
    return LogModel(
        Outcome=Outcome(dto.Outcome),
        Error=dto.Error,
        Email_id=ObjectId(dto.Email_id)
    )


def _from_log_model(model: LogModel) -> LogDTO:
    return LogDTO(
        Outcome=model.Outcome.value,
        Error=model.Error,
        Email_id=str(model.Email_id)
    )
