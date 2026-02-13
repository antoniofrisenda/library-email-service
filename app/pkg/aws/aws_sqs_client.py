import json
import boto3
from typing import Any
from app.pkg.util import get_env

class SQSClient:
    def __init__(self) -> None:
        self.queue_url = get_env("SQS_QUEUE")
        if not self.queue_url:
            raise ValueError("SQS_QUEUE env var required")
        
        self.sqs_client = boto3.client("sqs", endpoint_url=get_env("AWS_ENDPOINT_URL"),
            region_name=get_env("AWS_DEFAULT_REGION"),
            aws_access_key_id=get_env("AWS_ACCESS_KEY"),
            aws_secret_access_key=get_env("AWS_SECRET_KEY")
        )

    def receive_sqs_msg(self) -> dict[str, Any] | None:
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            WaitTimeSeconds=10,
            MaxNumberOfMessages=1
        )

        messages = response.get("Messages")
        if not messages:
            return None

        msg = messages[0]
        body = json.loads(msg["Body"])
        content = json.loads(body["Message"])

        self.sqs_client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=msg["ReceiptHandle"],
        )

        return content
