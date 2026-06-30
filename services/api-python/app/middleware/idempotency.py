import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse


class IdempotencyMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, redis_client):
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next):

        if request.method != "POST":
            return await call_next(request)

        idempotency_key = request.headers.get("Idempotency-Key")

        if not idempotency_key:
            return await call_next(request)

        cached = self.redis.get(idempotency_key)

        if cached:
            return JSONResponse(
                status_code=200,
                content=json.loads(cached),
            )

        response = await call_next(request)

        # store only successful responses
        if response.status_code < 400:
            body = b""

            async for chunk in response.body_iterator:
                body += chunk

            self.redis.setex(
                idempotency_key,
                3600,
                body.decode(),
            )

        return response