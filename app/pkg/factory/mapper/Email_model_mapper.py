from app.pkg.factory import EmailDTO
from app.pkg.domain import EmailModel, Type


def _to_email_model(dto: EmailDTO) -> EmailModel:
    return EmailModel(
        Type=Type(dto.Type),
        To=dto.To,
        Subject=dto.Subject,
        Body=dto.Body
    )


def _from_email_model(model: EmailModel) -> EmailDTO:
    return EmailDTO(
        Type=model.Type.value,
        To=model.To,
        Subject=model.Subject,
        Body=model.Body
    )
