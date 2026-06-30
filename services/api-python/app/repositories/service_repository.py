from sqlalchemy.orm import Session

from app.db.models import ServiceRequest


class ServiceRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        service_type: str,
        provider: str,
        payload: str,
        status: str = "PENDING",
    ) -> ServiceRequest:

        service_request = ServiceRequest(
            service_type=service_type,
            provider=provider,
            payload=payload,
            status=status,
        )

        self.db.add(service_request)
        self.db.commit()
        self.db.refresh(service_request)

        return service_request

    def get_by_id(
        self,
        request_id: str,
    ) -> ServiceRequest | None:

        return (
            self.db.query(ServiceRequest)
            .filter(ServiceRequest.id == request_id)
            .first()
        )

    def update_status(
        self,
        request_id: str,
        status: str,
    ) -> None:

        request = self.get_by_id(request_id)

        if request:
            request.status = status
            self.db.commit()