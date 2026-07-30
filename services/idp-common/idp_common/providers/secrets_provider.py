import json

import boto3

from botocore.exceptions import ClientError

from idp_common.config.settings import settings
from idp_common.providers.base import BaseProvider


class SecretsProvider(BaseProvider):

    def __init__(self):

        self.client = boto3.client(
            "secretsmanager",
            region_name=settings.AWS_REGION,
        )


    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        service_name = parameters.get(
            "service_name",
            resource_name,
        )

        environment = parameters.get(
            "environment",
            "default",
        )

        secret_name = parameters["secret_name"]

        if "/" not in secret_name:

            secret_name = (
                f"{service_name}/{environment}/{secret_name}"
            )

        secret_value = parameters["secret_value"]

        if not isinstance(secret_value, str):

            secret_value = json.dumps(secret_value)

        try:

            response = self.client.create_secret(
                Name=secret_name,
                SecretString=secret_value,
            )

            arn = response["ARN"]

        except self.client.exceptions.ResourceExistsException:

            self.client.put_secret_value(
                SecretId=secret_name,
                SecretString=secret_value,
            )

            arn = self.client.describe_secret(
                SecretId=secret_name,
            )["ARN"]

        return {
            "provider": "secretsmanager",
            "secret_name": secret_name,
            "secret_arn": arn,
            "status": "CREATED",
        }


    def deprovision(
        self,
        resource_id: str,
    ):

        self.client.delete_secret(
            SecretId=resource_id,
            ForceDeleteWithoutRecovery=True,
        )


    def get_status(
        self,
        resource_id: str,
    ):

        try:

            self.client.describe_secret(
                SecretId=resource_id,
            )

            return {
                "status": "ACTIVE",
            }

        except ClientError:
            return {
                "status": "NOT_FOUND",
            }