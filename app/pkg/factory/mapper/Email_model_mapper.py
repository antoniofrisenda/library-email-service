from app.pkg.factory import email_dto
from app.pkg.domain import Email, Type


def _to_email_model(dto: email_dto) -> Email:
    return Email(
        Type=Type(dto.Type),
        To=dto.To,
        Subject=dto.Subject,
        Body=dto.Body
    )


def _from_email_model(model: Email) -> email_dto:
    return email_dto(
        Type=model.Type.value,
        To=model.To,
        Subject=model.Subject,
        Body=model.Body
    )
