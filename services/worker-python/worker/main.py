import boto3

from jobs.executor import JobExecutor
from worker.provision_worker import ProvisionWorker

from idp_common.db.database import db_manager
from idp_common.messages.sqs_client import SQSClient
from idp_common.providers.factory import ProviderFactory
from idp_common.repositories.job_repository import JobRepository
from idp_common.repositories.service_repository import ServiceRepository


def run_worker():

    print("Worker started...")

    # Database
    db = db_manager.SessionLocal()

    # Repository
    job_repo = JobRepository(db)
    service_repo = ServiceRepository(db)

    # Business logic
    executor = JobExecutor(
        job_repo=job_repo,
        service_repo=service_repo,
        provider_factory=ProviderFactory,
    )

    # Messaging
    sqs_client = SQSClient()

    # Worker
    worker = ProvisionWorker(
        sqs_client=sqs_client,
        executor=executor,
    )

    try:
        while True:
            worker.poll()
    finally:
        db.close()


if __name__ == "__main__":
    run_worker()