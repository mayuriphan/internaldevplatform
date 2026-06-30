import boto3

from app.config.settings import settings
from app.providers.base import BaseProvider


class AWSProvider(BaseProvider):

    def __init__(self):

        self.session = boto3.session.Session(
            region_name=settings.AWS_REGION
        )

    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        return {
            "provider": "aws",
            "resource_name": resource_name,
            "status": "PROVISIONING",
        }

    def deprovision(
        self,
        resource_id: str,
    ):

        return {
            "resource_id": resource_id,
            "status": "DELETING",
        }

    def get_status(
        self,
        resource_id: str,
    ):

        return {
            "resource_id": resource_id,
            "status": "UNKNOWN",
        }