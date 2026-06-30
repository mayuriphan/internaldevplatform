from pydantic import BaseModel


class JobResponse(BaseModel):
    id: str
    status: str
    error_message: str | None = None