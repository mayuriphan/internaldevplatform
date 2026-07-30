import redis

from idp_common.config.settings import settings


class RedisAdmin:

    def __init__(self):

        kwargs = {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "decode_responses": True,
        }

        if settings.REDIS_PASSWORD:
            kwargs["password"] = settings.REDIS_PASSWORD

        self.client = redis.Redis(**kwargs)
        self.client.ping()


    def create_namespace(
        self,
        namespace: str,
    ):

        marker = f"{namespace}:provisioned"

        self.client.set(
            marker,
            "true",
        )

        return marker


    def namespace_exists(
        self,
        namespace: str,
    ):

        marker = f"{namespace}:provisioned"

        return self.client.exists(marker)