import time
from loguru import logger
from app.pkg.config import Receiver
from app.pkg.settings import create_instance


class SQSConsumer:
    def __init__(self):
        self.service = create_instance()
        self.receiver = Receiver()

    def consume_queue(self, msg: dict | None = None) -> None:
        logger.info("Consumer waiting...")
        msg = msg or self.receiver.receive_sqs_msg()

        while msg:
            logger.bind(message_type=msg.get("Type"), to=msg.get("To")).info("Received")

            try:
                self.service.consume_sqs_msg(msg)
                logger.bind(message_type=msg.get("Type"), to=msg.get("To")).info("SQS queue processed", payload=msg)
            finally:
                msg = self.receiver.receive_sqs_msg()

        logger.debug("Sleeping")
        time.sleep(2)
