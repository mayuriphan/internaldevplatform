import time

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


SKIP_PATHS = {
    "/health/live",
    "/health/ready",
    "/api/v1/login",
    "/docs",
    "/openapi.json",
    "/redoc",
}


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, redis_client, limit_per_minute: int = 60):
        super().__init__(app)
        self.redis = redis_client
        self.limit = limit_per_minute

    async def dispatch(self, request: Request, call_next):

        if request.url.path in SKIP_PATHS:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        key = f"rate:{client_ip}:{int(time.time() // 60)}"

        current = self.redis.get(key)

        if current and int(current) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers={"Retry-After": "60"},
            )

        pipe = self.redis.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, 60)
        pipe.execute()

        return await call_next(request)
