import os
import json
import boto3

QUEUE_URL = os.getenv("SQS_QUEUE")


class SQSClient:
    def __init__(self):
        self.sqs_client = boto3.client(
            "sqs",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        )

    def receive_sqs_message(self) -> dict | None:
        response = self.sqs_client.receive_message(
            QueueUrl=QUEUE_URL, 
            WaitTimeSeconds=2, 
            MaxNumberOfMessages=1, 
        ) 
        
        if "Messages" not in response: 
            return None 
        
        msg = response["Messages"][0] 
        body = json.loads(msg["Body"]) 
        content = json.loads(body["Message"]) 
        
        self.sqs_client.delete_message(
            QueueUrl=QUEUE_URL, 
            ReceiptHandle=msg["ReceiptHandle"], 
        ) 
        
        return content
