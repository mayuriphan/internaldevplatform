import json
import logging

from sqlalchemy.orm import Session

from app.services.job_service import JobService
from app.services.idempotency_service import IdempotencyService
from idp_common.repositories.outbox_repository import OutboxRepository
from idp_common.repositories.service_repository import ServiceRepository


logger = logging.getLogger("idp.broker")


class BrokerService:

    def __init__(
        self,
        db: Session,
        service_repo: ServiceRepository,
        job_service: JobService,
        idempotency_service: IdempotencyService,
        outbox_repo: OutboxRepository,
    ):
        self.db = db
        self.service_repo = service_repo
        self.job_service = job_service
        self.idempotency = idempotency_service
        self.outbox_repo = outbox_repo

    def provision(self, request: dict):

        key = self.idempotency.generate_key(request)

        cached = self.idempotency.get(key)
        if cached:
            return cached

        if not self.idempotency.try_claim(key):
            cached = self.idempotency.get(key)
            if cached:
                return cached
            return {
                "status": "PROCESSING",
                "detail": "An identical request is already being processed",
            }

        try:
            service_request = self.service_repo.create(
                service_type=request["service_type"],
                provider=request["provider"],
                payload=json.dumps(request),
                commit=False,
            )

            job = self.job_service.create_job(
                service_request.id,
                commit=False,
            )

            message = {
                "job_id": job.id,
                "request_id": service_request.id,
                "request": request,
            }

            self.outbox_repo.create(
                aggregate_type="job",
                aggregate_id=job.id,
                payload=json.dumps(message),
                commit=False,
            )

            self.db.commit()

            result = {
                "request_id": service_request.id,
                "job_id": job.id,
                "status": "QUEUED",
            }

            self.idempotency.store(key, result)
            logger.info(
                "provision_queued",
                extra={"job_id": job.id, "request_id": service_request.id},
            )

            return result

        except Exception:
            self.db.rollback()
            self.idempotency.release_claim(key)
            raise
