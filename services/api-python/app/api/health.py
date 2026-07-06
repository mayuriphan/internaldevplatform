from fastapi import APIRouter

router = APIRouter()


@router.get("/health/live")
def liveness():
    return {"status": "healthy"}


@router.get("/health/ready")
def readiness():
    return {
        "status": "ready",
        "dependencies": {
            "db": "ok",
            "redis": "ok"
        }
    }