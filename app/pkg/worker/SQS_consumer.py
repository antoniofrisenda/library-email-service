import time
from app.pkg.api import Instance
from app.pkg.config import Receiver


class SQSConsumer:
    def __init__(self):
        self.service = Instance()
        self.receiver = Receiver()

    def consume_queue(self, msg: dict | None = None):
        msg = msg or self.receiver.receive_sqs_msg()
        while msg:
            try:
                self.service.consume_sqs_msg(msg)
            finally:
                msg = self.receiver.receive_sqs_msg()
        time.sleep(2)