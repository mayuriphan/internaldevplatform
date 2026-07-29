import boto3

from jobs.executer import JobExecutor
from provision_worker import ProvisionWorker
from app.providers.factory import ProviderFactory
from app.repositories.job_repository import JobRepository
from app.db.database import db_manager


import boto3

sqs_client = boto3.client(
    "sqs",
    region_name="ap-south-1"
)

def process_message(message: dict):

    db = db_manager.SessionLocal()
    job_repo = JobRepository(db)

    executor = JobExecutor(
        job_repo=job_repo,
        provider_factory=ProviderFactory
    )

    executor.execute(message)


def run_worker():

    print("Worker started...")

    worker = ProvisionWorker(
        sqs_client=sqs_client,
        executor=executor
    )

    while True:
        worker.poll()


if __name__ == "__main__":
    run_worker()