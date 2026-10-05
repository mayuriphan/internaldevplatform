import json
import logging

from idp_common.config.settings import settings
from idp_common.db.database import db_manager
from idp_common.providers.factory import ProviderFactory
from idp_common.repositories.job_repository import JobRepository
from idp_common.repositories.service_repository import ServiceRepository
from jobs.executor import JobExecutor


logger = logging.getLogger("idp.worker")


class ProvisionWorker:

    def __init__(self, sqs_client):
        self.sqs = sqs_client

    def poll(self) -> None:

        messages = self.sqs.receive()

        if not messages:
            return

        logger.info("messages_received", extra={"count": len(messages)})

        for msg in messages:
            self._process_message(msg)

    def _process_message(self, msg: dict) -> None:

        receipt_handle = msg["ReceiptHandle"]
        receive_count = int(
            msg.get("Attributes", {}).get("ApproximateReceiveCount", "1")
        )

        try:
            body = json.loads(msg["Body"])
        except json.JSONDecodeError as exc:
            logger.error(
                "invalid_message_body",
                extra={"error": str(exc)},
            )
            if settings.SQS_DLQ_URL:
                self.sqs.send_to_dlq({"raw_body": msg["Body"], "error": str(exc)})
            self.sqs.delete(receipt_handle)
            return

        job_id = body.get("job_id", "unknown")

        db = db_manager.SessionLocal()

        try:
            executor = JobExecutor(
                job_repo=JobRepository(db),
                service_repo=ServiceRepository(db),
                provider_factory=ProviderFactory,
            )
            executor.execute(body)
            self.sqs.delete(receipt_handle)
            logger.info("message_processed", extra={"job_id": job_id})

        except Exception as exc:
            db.rollback()
            logger.exception(
                "message_processing_failed",
                extra={
                    "job_id": job_id,
                    "receive_count": receive_count,
                },
            )

            if receive_count >= settings.WORKER_MAX_RECEIVE_COUNT:
                logger.error(
                    "message_sent_to_dlq",
                    extra={"job_id": job_id, "receive_count": receive_count},
                )
                if settings.SQS_DLQ_URL:
                    body["_failure_reason"] = str(exc)
                    body["_receive_count"] = receive_count
                    self.sqs.send_to_dlq(body)
                self.sqs.delete(receipt_handle)
            # else: leave message on queue for SQS redelivery

        finally:
            db.close()
