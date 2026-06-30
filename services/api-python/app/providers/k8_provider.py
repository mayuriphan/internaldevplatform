from app.providers.base import BaseProvider


class KubernetesProvider(BaseProvider):

    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        return {
            "provider": "kubernetes",
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
            "status": "ACTIVE",
        }