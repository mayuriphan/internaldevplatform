import json

from app.providers.factory import ProviderFactory
from app.services.job_service import JobService
from app.services.idempotency_service import IdempotencyService
from app.repositories.service_repository import ServiceRepository


class BrokerService:

    def __init__(
        self,
        service_repo: ServiceRepository,
        job_service: JobService,
        idempotency_service: IdempotencyService,
        sqs_client=None,
    ):
        self.service_repo = service_repo
        self.job_service = job_service
        self.idempotency = idempotency_service
        self.sqs = sqs_client

    def provision(self, request: dict):

        # 1. Idempotency Key
        key = self.idempotency.generate_key(request)

        cached = self.idempotency.get(key)
        if cached:
            return cached

        # 2. Create Service Request
        service_request = self.service_repo.create(
            service_type=request["service_type"],
            provider=request["provider"],
            payload=json.dumps(request),
        )

        # 3. Create Job
        job = self.job_service.create_job(service_request.id)

        # 4. Send to queue (async execution)
        message = {
            "job_id": job.id,
            "request_id": service_request.id,
            "request": request,
        }

        if self.sqs:
            self.sqs.send_message(
                QueueUrl=self.sqs.queue_url,
                MessageBody=json.dumps(message),
            )

        result = {
            "request_id": service_request.id,
            "job_id": job.id,
            "status": "QUEUED",
        }

        # 5. Store idempotency result
        self.idempotency.store(key, result)

        return result