from .dto.DTO_log import LogDTO
from .dto.DTO_email import EmailDTO
from .mapper.Log_model_mapper import _to_log_model as log_model, _from_log_model as log_dto
from .mapper.Email_model_mapper import _to_email_model as email_model, _from_email_model as email_dto

__all__ = ["LogDTO", "EmailDTO", "log_model", "log_dto", "email_model", "email_dto"]
