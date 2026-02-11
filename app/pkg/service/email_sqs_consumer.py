import time
import logging
from app.pkg.config import Receiver
from app.pkg.service import create_service

logger = logging.getLogger(__name__)


class SQSConsumer:
    def __init__(self):
        self.service = create_service()
        self.receiver = Receiver()

    def consume_queue(self, msg: dict | None = None):
        logger.info("Consumer waiting...")
        msg = msg or self.receiver.receive_sqs_msg()
        while msg:
            logger.info("Received", extra={
                        "message_type": msg.get("Type"), "to": msg.get("To")},)
            try:
                self.service.consume_sqs_msg(msg)
                logger.info("SQS queue processed", extra={"payload": msg})
            finally:
                msg = self.receiver.receive_sqs_msg()
        logger.debug("sleeping")
        time.sleep(2)
