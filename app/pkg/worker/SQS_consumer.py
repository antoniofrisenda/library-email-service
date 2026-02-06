from app.pkg.api import instance
from app.pkg.config import receiver


class SQSConsumer:
    def __init__(self):
        self.service = instance()
        self.receiver = receiver()

    def consume_queue(self, msg: dict | None = None):
        msg = msg or self.receiver.receive_sqs_message()
        while msg:
            try:
                self.service.consume_message(msg)
            finally:
                msg = self.receiver.receive_sqs_message()
