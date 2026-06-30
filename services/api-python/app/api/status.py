from fastapi import APIRouter, Depends, HTTPException
from app.api.deps.db import get_db
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobResponse

router = APIRouter()


@router.get("/status/{job_id}", response_model=JobResponse)
def get_status(job_id: str, db=Depends(get_db)):

    repo = JobRepository(db)

    job = repo.get_by_id(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        id=job.id,
        status=job.status,
        error_message=job.error_message,
    )