from app.pkg.service.email_service import MailerService as Service
from app.pkg.service.email_sqs_consumer import SQSConsumer as Consumer

__all__ = ["Service", "Consumer"]
