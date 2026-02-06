import os
import json
import boto3


class SQSClient:
    def __init__(self):
        self.sqs_client = boto3.client(
            "sqs",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        )

        self.queue = os.getenv("SQS_QUEUE")

    def receive_sqs_message(self) -> dict | None:
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue,
            WaitTimeSeconds=2,
            MaxNumberOfMessages=1,
        )

        if "Messages" not in response:
            return None

        msg = response["Messages"][0]
        body = json.loads(msg["Body"])
        content = json.loads(body["Message"])

        self.sqs_client.delete_message(
            QueueUrl=self.queue,
            ReceiptHandle=msg["ReceiptHandle"],
        )

        return content
