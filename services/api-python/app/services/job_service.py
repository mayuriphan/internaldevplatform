from app.repositories.job_repository import JobRepository


class JobService:

    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def create_job(self, request_id: str):
        return self.job_repo.create(
            request_id=request_id,
            status="PENDING"
        )

    def mark_running(self, job_id: str):
        self.job_repo.update_status(
            job_id,
            status="RUNNING"
        )

    def mark_success(self, job_id: str):
        self.job_repo.update_status(
            job_id,
            status="SUCCESS"
        )

    def mark_failed(self, job_id: str, error: str):
        self.job_repo.update_status(
            job_id,
            status="FAILED",
            error_message=error
        )

    def get_job(self, job_id: str):
        return self.job_repo.get_by_id(job_id)