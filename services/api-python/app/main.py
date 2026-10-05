from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.provision import router as provision_router
from app.api.status import router as status_router
from app.db.redis import redis_client
from app.middleware.correlation_id import CorrelationIdMiddleware
from app.middleware.ratelimit import RateLimitMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from app.services.outbox_relay import OutboxRelay
from idp_common.config.settings import settings
from idp_common.db.database import init_db


outbox_relay = OutboxRelay()


@asynccontextmanager
async def lifespan(app: FastAPI):
    outbox_relay.start()
    yield
    outbox_relay.stop()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

init_db()


app.include_router(auth_router, prefix="/api/v1")
app.include_router(provision_router, prefix="/api/v1")
app.include_router(status_router, prefix="/api/v1")
app.include_router(health_router)


app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    redis_client=redis_client,
    limit_per_minute=settings.RATE_LIMIT_PER_MINUTE,
)
