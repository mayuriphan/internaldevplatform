import json

from app.jobs.executor import JobExecutor


class ProvisionWorker:

    def __init__(self, sqs_client, executor: JobExecutor):
        self.sqs = sqs_client
        self.executor = executor

    def poll(self):

        messages = self.sqs.receive_messages()

        for msg in messages:

            body = json.loads(msg["Body"])

            self.executor.execute(body)

            self.sqs.delete_message(msg)