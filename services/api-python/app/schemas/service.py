from pydantic import BaseModel
from typing import List

class ProvisionParameters(BaseModel):
    service_name: str
    environment: str
    template: str
    replicas: int
    cpu: str
    memory: str
    features: List[str]


class ProvisionRequest(BaseModel):
    service_type: str
    provider: str
    parameters: ProvisionParameters


class ProvisionResponse(BaseModel):
    request_id: str
    job_id: str
    status: str