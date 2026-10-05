from app.db.redis import redis_client
from app.services.broker_service import BrokerService
from app.services.idempotency_service import IdempotencyService
from app.services.job_service import JobService
from fastapi import Depends
from idp_common.db.database import get_db
from idp_common.repositories.job_repository import JobRepository
from idp_common.repositories.outbox_repository import OutboxRepository
from idp_common.repositories.service_repository import ServiceRepository
from sqlalchemy.orm import Session


def get_broker_service(db: Session = Depends(get_db)):

    service_repo = ServiceRepository(db)
    job_repo = JobRepository(db)
    outbox_repo = OutboxRepository(db)

    job_service = JobService(job_repo)
    idempotency_service = IdempotencyService(redis_client)

    return BrokerService(
        db=db,
        service_repo=service_repo,
        job_service=job_service,
        idempotency_service=idempotency_service,
        outbox_repo=outbox_repo,
    )
