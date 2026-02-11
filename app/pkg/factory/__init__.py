from app.pkg.factory.dto.email_document_payload import EmailDTO as Dto
from app.pkg.factory.mapper.email_model_mapper import _to_email_model as email_model, _from_email_model as email_dto

__all__ = ["Dto", "email_model", "email_dto"]
