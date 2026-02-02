from app.pkg.factory import EmailDTO
from app.pkg.domain import EmailModel, Type


def _to_email_model(dto: EmailDTO) -> EmailModel:
    return EmailModel(
        type=Type(dto.type),
        to=dto.to,
        body=dto.body
    )


def _from_email_model(model: EmailModel) -> EmailDTO:
    return EmailDTO(
        type=model.type.value,
        to=model.to,
        body=model.body
    )
