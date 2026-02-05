from .model.Email_mongo_model import EmailModel, EmailType as Type
from .model.Log_mongo_model import LogModel, EmailOutcome as Outcome

__all__ = ["LogModel", "EmailModel", "Outcome", "Type"]
