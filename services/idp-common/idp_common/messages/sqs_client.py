import json

import boto3

from idp_common.config.settings import settings


class SQSClient:

    def __init__(self):

        self.client = boto3.client(
            "sqs",
            region_name=settings.AWS_REGION,
        )

        self.job_queue = settings.SQS_JOBQ_URL
        self.dlq = settings.SQS_DLQ_URL

    def send(self, message: dict):

        print("Sending to SQS:", message)

        self.client.send_message(
        QueueUrl=self.job_queue,
        MessageBody=json.dumps(message),
    )

    def receive(self, max_messages: int = 10):

        response = self.client.receive_message(
        QueueUrl=self.job_queue,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20,
    )

        return response.get("Messages", [])
    
    def delete(self, receipt_handle: str):

        self.client.delete_message(
            QueueUrl=self.job_queue,
            ReceiptHandle=receipt_handle,
        )

    def send_to_dlq(self, message: dict):

        self.client.send_message(
            QueueUrl=self.dlq,
            MessageBody=json.dumps(message),
        )