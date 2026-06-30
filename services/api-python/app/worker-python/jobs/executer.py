import json


class JobExecutor:

    def __init__(self, job_repo, provider_factory):
        self.job_repo = job_repo
        self.provider_factory = provider_factory

    def execute(self, message: dict):

        job_id = message["job_id"]
        request = message["request"]

        try:
            # 1. Mark RUNNING
            self.job_repo.update_status(job_id, "RUNNING")

            # 2. Select provider dynamically
            provider = self.provider_factory.create(
                request["provider"]
            )

            # 3. Execute provisioning
            result = provider.provision(
                resource_name=request["service_type"],
                parameters=request.get("parameters", {})
            )

            # 4. Mark SUCCESS
            self.job_repo.update_status(job_id, "SUCCESS")

            print(f"Job {job_id} completed: {result}")

        except Exception as e:

            # 5. Mark FAILED
            self.job_repo.update_status(
                job_id,
                "FAILED",
                error_message=str(e)
            )

            print(f"Job {job_id} failed: {str(e)}")