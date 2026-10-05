import logging
import threading

from idp_common.config.settings import settings
from idp_common.messages.outbox_publisher import OutboxPublisher


logger = logging.getLogger("idp.outbox_relay")


class OutboxRelay:

    def __init__(self):
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._publisher = OutboxPublisher()

    def _run(self) -> None:

        logger.info("outbox_relay_started")

        while not self._stop.is_set():
            try:
                self._publisher.publish_batch()
            except Exception:
                logger.exception("outbox_relay_error")

            self._stop.wait(settings.OUTBOX_POLL_INTERVAL_SECONDS)

        logger.info("outbox_relay_stopped")

    def start(self) -> None:

        if self._thread and self._thread.is_alive():
            return

        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="outbox-relay",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)
