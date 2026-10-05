from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Session

from idp_common.models.outbox import OutboxMessage


class OutboxRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        aggregate_type: str,
        aggregate_id: str,
        payload: str,
        commit: bool = True,
    ) -> OutboxMessage:

        message = OutboxMessage(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            payload=payload,
            status="PENDING",
        )

        self.db.add(message)

        if commit:
            self.db.commit()
            self.db.refresh(message)
        else:
            self.db.flush()

        return message

    def get_pending(self, limit: int = 10) -> list[OutboxMessage]:

        return (
            self.db.query(OutboxMessage)
            .filter(OutboxMessage.status == "PENDING")
            .order_by(OutboxMessage.created_at)
            .limit(limit)
            .all()
        )

    def mark_sent(self, message_id: str) -> None:

        message = self.db.get(OutboxMessage, message_id)
        if not message:
            return

        message.status = "SENT"
        message.processed_at = datetime.now(timezone.utc)
        self.db.commit()

    def mark_failed(
        self,
        message_id: str,
        error_message: str,
        max_retries: int,
    ) -> None:

        message = self.db.get(OutboxMessage, message_id)
        if not message:
            return

        message.retry_count += 1
        message.error_message = error_message

        if message.retry_count >= max_retries:
            message.status = "FAILED"
            message.processed_at = datetime.now(timezone.utc)

        self.db.commit()
