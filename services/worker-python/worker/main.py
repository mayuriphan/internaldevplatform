import json
import time

from jobs.executer import JobExecutor
from app.providers.factory import ProviderFactory
from app.repositories.job_repository import JobRepository
from app.db.database import db_manager


def process_message(message: dict):

    db = db_manager.SessionLocal()
    job_repo = JobRepository(db)

    executor = JobExecutor(
        job_repo=job_repo,
        provider_factory=ProviderFactory
    )

    executor.execute(message)


def run_worker():

    print("Worker started... listening for jobs")

    while True:
        fake_message = None

        if fake_message:
            process_message(json.loads(fake_message))

        time.sleep(2)


if __name__ == "__main__":
    run_worker()