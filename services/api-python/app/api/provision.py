from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.api.deps.auth import get_current_user
from app.api.deps.broker import get_broker_service
from app.schemas.service import ProvisionRequest
from app.schemas.service import ProvisionResponse


router = APIRouter()


@router.post("/provision", response_model=ProvisionResponse)
def provision(
    request: ProvisionRequest,
    broker=Depends(get_broker_service),
    _user=Depends(get_current_user),
):

    result = broker.provision(request.model_dump())

    if result.get("status") == "PROCESSING":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result.get("detail", "Request already in progress"),
        )

    return ProvisionResponse(
        request_id=result["request_id"],
        job_id=result["job_id"],
        status=result["status"],
    )