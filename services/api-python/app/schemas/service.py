from typing import Any
from typing import List

from pydantic import BaseModel

class ProvisionParameters(BaseModel):
    service_name: str
    environment: str

    template: str | None = None
    replicas: int | None = None
    cpu: str | None = None
    memory: str | None = None

    features: List[str] = []

    secret_name: str | None = None
    secret_value: dict[str, Any] | str | None = None


class ProvisionRequest(BaseModel):
    service_type: str
    provider: str
    parameters: ProvisionParameters


class ProvisionResponse(BaseModel):
    request_id: str
    job_id: str
    status: str