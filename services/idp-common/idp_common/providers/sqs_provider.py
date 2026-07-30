import json

import boto3

from idp_common.config.settings import settings
from idp_common.providers.base import BaseProvider


class SQSProvider(BaseProvider):

    def __init__(self):

        self.client = boto3.client(
            "sqs",
            region_name=settings.AWS_REGION,
        )

    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        service_name = parameters["service_name"]
        environment = parameters["environment"]

        queue_name = (
            f"{service_name}-{environment}"
            .replace("_", "-")
            .lower()
        )

        dlq_name = f"{queue_name}-dlq"

        # Create DLQ
        dlq = self.client.create_queue(
            QueueName=dlq_name,
        )

        dlq_url = dlq["QueueUrl"]

        dlq_arn = self.client.get_queue_attributes(
            QueueUrl=dlq_url,
            AttributeNames=["QueueArn"],
        )["Attributes"]["QueueArn"]

        # Create Main Queue
        queue = self.client.create_queue(
            QueueName=queue_name,
            Attributes={
                "RedrivePolicy": json.dumps(
                    {
                        "deadLetterTargetArn": dlq_arn,
                        "maxReceiveCount": 5,
                    }
                )
            },
        )

        queue_url = queue["QueueUrl"]

        queue_arn = self.client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=["QueueArn"],
        )["Attributes"]["QueueArn"]

        return {
            "provider": "sqs",
            "queue_name": queue_name,
            "queue_url": queue_url,
            "queue_arn": queue_arn,
            "dlq": dlq_name,
            "status": "CREATED",
        }

    def deprovision(
        self,
        resource_id: str,
    ):

        self.client.delete_queue(
            QueueUrl=resource_id,
        )

    def get_status(
        self,
        resource_id: str,
    ):

        try:

            self.client.get_queue_attributes(
                QueueUrl=resource_id,
                AttributeNames=["QueueArn"],
            )

            return {
                "status": "ACTIVE",
            }

        except Exception:

            return {
                "status": "NOT_FOUND",
            }