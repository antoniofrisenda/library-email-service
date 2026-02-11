from app.pkg.factory import Dto
from app.pkg.domain import Email, Type


def _to_email_model(dto: Dto) -> Email:
    return Email(
        Type=Type(dto.Type),
        To=dto.To,
        Subject=dto.Subject,
        Body=dto.Body
    )


def _from_email_model(model: Email) -> Dto:
    return Dto(
        Type=model.Type.value,
        To=model.To,
        Subject=model.Subject,
        Body=model.Body
    )
