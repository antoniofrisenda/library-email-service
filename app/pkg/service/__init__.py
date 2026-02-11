from app.pkg.service.email_service import MailerService as Service
from app.pkg.service.email_sqs_consumer import SQSConsumer as Consumer
from app.pkg.service.service_wrapper import _create_service as create_service

__all__ = ["Service", "create_service", "Consumer"]