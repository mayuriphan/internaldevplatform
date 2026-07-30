from app.db.redis import redis_client
from idp_common.db.database import get_db
from idp_common.messages.sqs_client import SQSClient
from idp_common.repositories.service_repository import ServiceRepository
from idp_common.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.services.broker_service import BrokerService
from app.services.idempotency_service import IdempotencyService

from fastapi import Depends
from sqlalchemy.orm import Session


def get_broker_service(db: Session = Depends(get_db)):

    sqs_client = SQSClient()

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