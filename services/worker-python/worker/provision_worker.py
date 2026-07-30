import json

from jobs.executor import JobExecutor


class ProvisionWorker:

    def __init__(self, sqs_client, executor: JobExecutor):
        self.sqs = sqs_client
        self.executor = executor

    def poll(self):
        print("Polling SQS...")

        messages = self.sqs.receive()

        print(f"Received {len(messages)} messages")

        for msg in messages:

            body = json.loads(msg["Body"])

            self.executor.execute(body)

            self.sqs.delete(msg["ReceiptHandle"])