from fastapi import FastAPI

from app.api.provision import router as provision_router
from app.api.status import router as status_router
from app.api.health import router as health_router

from app.middleware.correlation_id import CorrelationIdMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.ratelimit import RateLimitMiddleware

from app.config.settings import settings


app = FastAPI(title=settings.APP_NAME)


# Routers
app.include_router(provision_router, prefix="/api/v1")
app.include_router(status_router, prefix="/api/v1")
app.include_router(health_router)


# Middleware (order matters)
# 1. correlation id
app.add_middleware(CorrelationIdMiddleware)

# 2. logging
app.add_middleware(RequestLoggingMiddleware)

# 3. rate limiting (requires redis client injection later in real setup)
# app.add_middleware(RateLimitMiddleware, redis_client=redis)