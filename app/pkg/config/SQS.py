import os
import json
import boto3

sqs = boto3.client(
    "sqs",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
)

QUEUE_URL = os.getenv("SQS_QUEUE")


def receive_sqs_message() -> dict | None:
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        WaitTimeSeconds=2,
        MaxNumberOfMessages=1,
    )

    if "Messages" not in response:
        return None

    msg = response["Messages"][0]
    body = json.loads(msg["Body"])
    content = json.loads(body["Message"])

    sqs.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=msg["ReceiptHandle"],
    )

    return content
