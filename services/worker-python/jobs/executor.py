import json


class JobExecutor:

    def __init__(self, job_repo,  service_repo, provider_factory):
        self.job_repo = job_repo
        self.service_repo = service_repo
        self.provider_factory = provider_factory

    def execute(self, message: dict):

        job_id = message["job_id"]
        request = message["request"]
        request_id = message["request_id"]

        try:
            # 1. Mark RUNNING
            self.job_repo.update_status(job_id, "RUNNING")
            self.service_repo.update_status(request_id, "RUNNING")

            # 2. Select provider dynamically
            provider = self.provider_factory.create(
                request["provider"]
            )

            # 3. Execute provisioning
            parameters = request["parameters"].copy()
            parameters["service_type"] = request["service_type"]
            resource_name = parameters["service_name"]

            result = provider.provision(
                resource_name=resource_name,
                parameters=parameters,
            )

            # 4. Mark SUCCESS
            self.job_repo.update_status(job_id, "SUCCESS")
            self.service_repo.update_status(request_id, "SUCCESS")

            print(f"Job {job_id} completed: {result}")

        except Exception as e:

            # 5. Mark FAILED
            self.job_repo.update_status(
                job_id,
                "FAILED",
                error_message=str(e)
            )
            self.service_repo.update_status(
                request_id,
                "FAILED",
            )

            # print(f"Job {job_id} failed: {str(e)}")
            raise