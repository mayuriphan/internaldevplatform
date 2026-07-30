from idp_common.config.settings import settings
from idp_common.db.redis_admin import RedisAdmin
from idp_common.providers.base import BaseProvider


class RedisProvider(BaseProvider):

    def __init__(self):

        self.admin = RedisAdmin()


    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        namespace = (
            f'{parameters["service_name"]}_'
            f'{parameters["environment"]}'
        ).replace("-", "_")

        self.admin.create_namespace(
            namespace
        )

        print(f"Created Redis namespace {namespace}")

        return {
            "provider": "redis",
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "namespace": namespace,
            "status": "READY",
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

        exists = self.admin.namespace_exists(
            resource_id
        )

        return {
            "namespace": resource_id,
            "exists": bool(exists),
        }