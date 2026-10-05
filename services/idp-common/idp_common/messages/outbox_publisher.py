import json
import logging

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from idp_common.config.settings import settings
from idp_common.db.database import db_manager
from idp_common.messages.sqs_client import SQSClient
from idp_common.repositories.outbox_repository import OutboxRepository


logger = logging.getLogger("idp.outbox")


class OutboxPublisher:

    def __init__(self, sqs_client: SQSClient | None = None):
        self.sqs = sqs_client or SQSClient()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    def _send(self, payload: dict) -> None:
        self.sqs.send(payload)

    def publish_batch(self) -> int:

        db = db_manager.SessionLocal()
        published = 0

        try:
            repo = OutboxRepository(db)
            pending = repo.get_pending(limit=settings.OUTBOX_BATCH_SIZE)

            for message in pending:
                try:
                    payload = json.loads(message.payload)
                    self._send(payload)
                    repo.mark_sent(message.id)
                    published += 1
                    logger.info(
                        "outbox_published",
                        extra={"outbox_id": message.id, "aggregate_id": message.aggregate_id},
                    )
                except Exception as exc:
                    logger.exception(
                        "outbox_publish_failed",
                        extra={"outbox_id": message.id},
                    )
                    repo.mark_failed(
                        message.id,
                        str(exc),
                        max_retries=settings.OUTBOX_MAX_RETRIES,
                    )
        finally:
            db.close()

        return published
