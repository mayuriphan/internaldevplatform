import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from app.db.database import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    service_type = Column(String(100), nullable=False)

    provider = Column(String(100), nullable=False)

    status = Column(String(50), nullable=False)

    payload = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    request_id = Column(
        String(36),
        nullable=False,
    )

    status = Column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    error_message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )