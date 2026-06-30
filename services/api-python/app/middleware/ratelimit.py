import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, redis_client, limit_per_minute: int = 60):
        super().__init__(app)
        self.redis = redis_client
        self.limit = limit_per_minute

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host
        key = f"rate:{client_ip}:{int(time.time() // 60)}"

        current = self.redis.get(key)

        if current and int(current) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
            )

        pipe = self.redis.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, 60)
        pipe.execute()

        return await call_next(request)