from typing import Any
from typing import Dict

from pydantic import BaseModel


class ProvisionRequest(BaseModel):
    service_type: str
    provider: str
    parameters: Dict[str, Any]


class ProvisionResponse(BaseModel):
    request_id: str
    job_id: str
    status: str