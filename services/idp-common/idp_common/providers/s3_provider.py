import boto3

from idp_common.config.settings import settings
from idp_common.providers.base import BaseProvider


class S3Provider(BaseProvider):

    def __init__(self):

        self.client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
        )

    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        service_name = parameters["service_name"]
        environment = parameters["environment"]

        bucket_name = (
            f"{service_name}-{environment}"
            .replace("_", "-")
            .lower()
        )

        existing = self.client.list_buckets()["Buckets"]

        if bucket_name not in [
            bucket["Name"]
            for bucket in existing
        ]:

            self.client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                "LocationConstraint": settings.AWS_REGION,
                },
            )

            self.client.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={
                    "TagSet": [
                        {
                            "Key": "managed-by",
                            "Value": "idp",
                        },
                        {
                            "Key": "service",
                            "Value": service_name,
                        },
                    ]
                },
            )

        return {
            "provider": "s3",
            "bucket": bucket_name,
            "status": "CREATED",
        }

    def deprovision(
        self,
        resource_id: str,
    ):

        self.client.delete_bucket(
            Bucket=resource_id,
        )

    def get_status(
        self,
        resource_id: str,
    ):

        try:

            self.client.head_bucket(
                Bucket=resource_id,
            )

            return {
                "status": "ACTIVE",
            }

        except Exception:

            return {
                "status": "NOT_FOUND",
            }