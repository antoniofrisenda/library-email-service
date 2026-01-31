from app.pkg.factory import EmailDTO
from app.pkg.domain import EmailModel, EmailTypeEnum

def dto_to_email(dto: EmailDTO) -> EmailModel:
    return EmailModel(
        email_type=EmailTypeEnum(dto.email_type),
        address_to=dto.address_to,
        body_fields=dto.body_fields
    )

def email_to_dto(model: EmailModel) -> EmailDTO:
    return EmailDTO(
        email_type=model.email_type.value,
        address_to=model.address_to,
        body_fields=model.body_fields
    )
