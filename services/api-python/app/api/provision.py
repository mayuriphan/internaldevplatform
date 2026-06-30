from fastapi import APIRouter, Depends
from app.schemas.service import ProvisionRequest, ProvisionResponse
from app.api.deps.broker import get_broker_service

router = APIRouter()


@router.post("/provision", response_model=ProvisionResponse)
def provision(
    request: ProvisionRequest,
    broker = Depends(get_broker_service),
):

    result = broker.provision(request.model_dump())

    return ProvisionResponse(
        request_id=result["request_id"],
        job_id=result["job_id"],
        status=result["status"],
    )