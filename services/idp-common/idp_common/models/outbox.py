import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from idp_common.db.database import Base


class OutboxMessage(Base):

    __tablename__ = "outbox_messages"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    aggregate_type = Column(String(50), nullable=False)
    aggregate_id = Column(String(36), nullable=False)

    payload = Column(Text, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    retry_count = Column(Integer, nullable=False, default=0)
    error_message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    processed_at = Column(DateTime(timezone=True))
