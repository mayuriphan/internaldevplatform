from idp_common.providers.aws_provider import AWSProvider
from idp_common.providers.k8_provider import KubernetesProvider
from idp_common.providers.postgres_provider import PostgresProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name: str):

        providers = {
            "aws": AWSProvider,
            "postgres": PostgresProvider,
            "kubernetes": KubernetesProvider,
        }

        provider_class = providers.get(provider_name)

        if provider_class is None:
            raise ValueError(
                f"Unsupported provider: {provider_name}"
            )

        return provider_class()