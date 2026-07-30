from idp_common.providers.aws_provider import AWSProvider
from idp_common.providers.k8_provider import KubernetesProvider
from idp_common.providers.postgres_provider import PostgresProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name: str):

        providers = {
            "aws": AWSProvider,
            # "azure": AzureProvider,
            # "gcp": GCPProvider,
        }

        provider = providers.get(provider_name)

        if provider is None:
            raise ValueError(
                f"Unsupported provider: {provider_name}"
            )

        return provider()