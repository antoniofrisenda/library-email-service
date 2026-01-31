from bson import ObjectId
from datetime import datetime
from app.pkg.factory import EmailDTO
from app.pkg.domain import EmailModel, EmailTypeEnum


@classmethod
def email_to_dto(email: EmailModel) -> EmailDTO:
    return EmailDTO(
        id=str(email.id),
        email_type=email.email_type.value,
        address_to=email.address_to,
        body_fields=email.body_fields,
        sent_at=email.sent_at.isoformat()
    )


def dto_to_email(dto: EmailDTO) -> EmailModel:
    return EmailModel(
        id=ObjectId(dto.id),
        email_type=EmailTypeEnum(dto.email_type),
        address_to=dto.address_to,
        body_fields=dto.body_fields,
        sent_at=datetime.fromisoformat(dto.sent_at)
    )
