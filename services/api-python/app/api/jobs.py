from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.jobs import JobCreate
from app.db.database import get_db
from app.services.job_service import JobService

router = APIRouter()
service = JobService()

@router.post("/")
def create_job(req: JobCreate, db: Session = Depends(get_db)):
    return service.create_job(db, req.dict())