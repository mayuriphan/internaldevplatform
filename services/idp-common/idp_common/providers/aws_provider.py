from idp_common.providers.base import BaseProvider
from idp_common.providers.postgres_provider import PostgresProvider
from idp_common.providers.redis_provider import RedisProvider
from idp_common.providers.k8_provider import KubernetesProvider


class AWSProvider(BaseProvider):

    def __init__(self):

        self.postgres = PostgresProvider()
        self.redis = RedisProvider()
        self.kubernetes = KubernetesProvider()


    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):

        resources = {}

        features = parameters.get(
            "features",
            [],
        )

        if "postgres" in features:

            resources["postgres"] = (
                self.postgres.provision(
                    resource_name,
                    parameters,
                )
            )

        if "redis" in features:

            resources["redis"] = (
                self.redis.provision(
                    resource_name,
                    parameters,
                )
            )

        runtime = parameters.get(
            "runtime",
            "kubernetes",
        )

        if runtime == "kubernetes":

            resources["runtime"] = (
                self.kubernetes.provision(
                    resource_name,
                    parameters,
                )
            )

        elif runtime == "ecs":

            resources["runtime"] = {
                "status": "NOT_IMPLEMENTED"
            }

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