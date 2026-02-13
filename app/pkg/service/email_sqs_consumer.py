import time
import logging
from app.pkg.aws import Receiver
from app.pkg.service import Service
from app.pkg.repository import Repo
from app.pkg.mongo import Connection


logger = logging.getLogger("app")


class SQSConsumer:
    def __init__(self) -> None:
        try:
            self.service = Service(Repo(Connection().get_db()))
            self.receiver = Receiver()
            logger.info("Consumer init OK")
        except Exception:
            logger.warning("init Consumer failed")
            raise

    def consume_queue(self) -> None:
        logger.info("Consumer waiting...")

        while True:
            msg = self.receiver.receive_sqs_msg()

            if not msg:
                logger.info("Sleeping")
                time.sleep(2)
                continue

            logger.info(
                f"Received | "f"raw mgs={msg}" f"message_type={msg.get('Type')} " f"to={msg.get('To')}")

            try:
                self.service.consume_sqs_msg(msg)
                logger.info(f"SQS queue processed")

            except Exception:
                logger.warning(f"Message: {msg} not processed")
