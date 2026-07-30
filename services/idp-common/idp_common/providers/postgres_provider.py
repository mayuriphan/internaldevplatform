from idp_common.config.settings import settings
from idp_common.providers.base import BaseProvider
from idp_common.db.postgres_admin import PostgresAdmin
from idp_common.utils.secrets import generate_password
from idp_common.providers.secrets_provider import SecretsProvider


class PostgresProvider(BaseProvider):

    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):
        service_name = parameters["service_name"]
        database_name = f"{service_name}_{settings.ENVIRONMENT}"
        username = (
            f"{service_name.replace('-', '_')}_{settings.ENVIRONMENT}"
        )
        password = generate_password()
        admin = PostgresAdmin()

        admin.create_database(
            database_name
        )

        admin.create_user(
            username,
            password,
            database_name
        )

        secret = SecretsProvider().provision(

            resource_name,

            {
                "secret_name": f"{database_name}-credentials",

                "secret_value": {

                    "host": settings.POSTGRES_HOST,

                    "port": settings.POSTGRES_PORT,

                    "database": database_name,

                    "username": username,

                    "password": password,
                },
            },
        )

        return {
            "provider": "postgres",
            "resource_name": database_name,
            "secret": secret,
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT,
            "status": "CREATED",
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
            "status": "RUNNING",
        }