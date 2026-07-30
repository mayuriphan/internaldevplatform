from idp_common.providers.base import BaseProvider
from idp_common.providers.postgres_provider import PostgresProvider
from idp_common.providers.redis_provider import RedisProvider
from idp_common.providers.s3_provider import S3Provider
from idp_common.providers.sqs_provider import SQSProvider
from idp_common.providers.secrets_provider import SecretsProvider
# from idp_common.providers.iam_provider import IAMProvider


class AWSProvider(BaseProvider):

    def __init__(self):

        self.providers = {
            "postgres": PostgresProvider(),
            "redis": RedisProvider(),
            "s3": S3Provider(),
            "sqs": SQSProvider(),
            "secret": SecretsProvider(),
            # "iam": IAMProvider(),
        }

    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        resources = {}

        service_type = parameters.get("service_type")
        if service_type == "secret":

            result = self.providers["secret"].provision(
                resource_name,
                parameters,
            )

            return {
                "provider": "aws",
                "resource_name": resource_name,
                "status": "SUCCESS",
                "resources": {
                    "secret": result
                },
            }

        features = parameters.get("features", [])

        for feature in features:

            provider = self.providers.get(feature)

            if provider is None:
                continue

            resources[feature] = provider.provision(
                resource_name,
                parameters,
            )

        return {
            "provider": "aws",
            "resource_name": resource_name,
            "status": "SUCCESS",
            "resources": resources,
        }

    def deprovision(
        self,
        resource_id: str,
    ):

        return {
            "status": "NOT_IMPLEMENTED",
        }

    def get_status(
        self,
        resource_id: str,
    ):

        return {
            "status": "UNKNOWN",
        }