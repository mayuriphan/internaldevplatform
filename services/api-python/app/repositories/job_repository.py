from sqlalchemy.orm import Session

from app.db.models import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        request_id: str,
        status: str = "PENDING",
    ) -> Job:

        job = Job(
            request_id=request_id,
            status=status,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get_by_id(
        self,
        job_id: str,
    ) -> Job | None:

        return (
            self.db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

    def update_status(
        self,
        job_id: str,
        status: str,
        error_message: str | None = None,
    ) -> None:

        job = self.get_by_id(job_id)

        if not job:
            return

        job.status = status
        job.error_message = error_message

        self.db.commit()

    def list_pending_jobs(self):

        return (
            self.db.query(Job)
            .filter(Job.status == "PENDING")
            .all()
        )