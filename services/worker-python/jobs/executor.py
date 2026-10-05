import logging

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from idp_common.config.settings import settings
from idp_common.utils.retry import retry_on_transient_aws


logger = logging.getLogger("idp.executor")


class JobExecutor:

    def __init__(self, job_repo, service_repo, provider_factory):
        self.job_repo = job_repo
        self.service_repo = service_repo
        self.provider_factory = provider_factory

    @retry(
        stop=stop_after_attempt(settings.PROVISION_MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_on_transient_aws,
        reraise=True,
    )
    def _provision_with_retry(self, provider, resource_name, parameters):
        return provider.provision(
            resource_name=resource_name,
            parameters=parameters,
        )

    def execute(self, message: dict) -> None:

        job_id = message["job_id"]
        request = message["request"]
        request_id = message["request_id"]

        self.job_repo.update_status(job_id, "RUNNING")
        self.service_repo.update_status(request_id, "RUNNING")

        try:
            provider = self.provider_factory.create(request["provider"])

            parameters = request["parameters"].copy()
            parameters["service_type"] = request["service_type"]
            resource_name = parameters["service_name"]

            result = self._provision_with_retry(
                provider,
                resource_name,
                parameters,
            )

            self.job_repo.update_status(job_id, "SUCCESS")
            self.service_repo.update_status(request_id, "SUCCESS")

            logger.info(
                "job_completed",
                extra={"job_id": job_id, "result_status": result.get("status")},
            )

        except Exception as exc:
            self.job_repo.update_status(
                job_id,
                "FAILED",
                error_message=str(exc),
            )
            self.service_repo.update_status(request_id, "FAILED")

            logger.exception(
                "job_failed",
                extra={"job_id": job_id, "request_id": request_id},
            )
            raise exc
