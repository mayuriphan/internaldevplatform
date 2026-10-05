import logging
import signal
import sys

from idp_common.messages.sqs_client import SQSClient
from worker.provision_worker import ProvisionWorker


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

logger = logging.getLogger("idp.worker.main")

_running = True


def _handle_shutdown(signum, frame):
    global _running
    logger.info("shutdown_signal_received", extra={"signal": signum})
    _running = False


def run_worker():

    signal.signal(signal.SIGTERM, _handle_shutdown)
    signal.signal(signal.SIGINT, _handle_shutdown)

    logger.info("worker_started")

    sqs_client = SQSClient()
    worker = ProvisionWorker(sqs_client=sqs_client)

    try:
        while _running:
            worker.poll()
    except Exception:
        logger.exception("worker_crashed")
        sys.exit(1)
    finally:
        logger.info("worker_stopped")


if __name__ == "__main__":
    run_worker()
