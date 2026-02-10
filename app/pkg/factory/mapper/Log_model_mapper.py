from bson import ObjectId
from app.pkg.factory import log_dto
from app.pkg.domain import Log, Outcome


def _to_log_model(dto: log_dto) -> Log:
    return Log(
        Outcome=Outcome(dto.Outcome),
        Error=dto.Error,
        Email_id=ObjectId(dto.Email_id)
    )


def _from_log_model(model: Log) -> log_dto:
    return log_dto(
        Outcome=model.Outcome.value,
        Error=model.Error,
        Email_id=str(model.Email_id)
    )
