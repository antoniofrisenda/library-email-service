from app.pkg.service.email_sqs_consumer import SQSConsumer as Consumer
from app.pkg.service.email_sender_service import MailerService as Service

__all__ = ["Service", "Consumer"]
