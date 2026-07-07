from app.db.database import get_db
from app.db.redis import redis_client
from app.repositories.service_repository import ServiceRepository
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.services.broker_service import BrokerService
from app.services.idempotency_service import IdempotencyService


def get_broker_service():

    sqs_client = None

    db = get_db()
    service_repo = ServiceRepository(db)
    job_repo = JobRepository(db)

    job_service = JobService(job_repo)
    idempotency_service = IdempotencyService(redis_client)

    return BrokerService(
        service_repo=service_repo,
        job_service=job_service,
        idempotency_service=idempotency_service,
        sqs_client=sqs_client,
    )