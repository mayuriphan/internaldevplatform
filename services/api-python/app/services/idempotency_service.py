import hashlib
import json


class IdempotencyService:

    KEY_PREFIX = "idempotency:"

    def __init__(self, redis_client):
        self.redis = redis_client

    def _redis_key(self, key: str) -> str:
        return f"{self.KEY_PREFIX}{key}"

    def generate_key(self, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def try_claim(self, key: str, ttl_seconds: int = 3600) -> bool:
        return bool(
            self.redis.set(
                self._redis_key(key),
                json.dumps({"status": "PROCESSING"}),
                nx=True,
                ex=ttl_seconds,
            )
        )

    def release_claim(self, key: str) -> None:
        self.redis.delete(self._redis_key(key))

    def store(self, key: str, value: dict, ttl_seconds: int = 3600):
        self.redis.setex(
            self._redis_key(key),
            ttl_seconds,
            json.dumps(value),
        )

    def get(self, key: str):
        data = self.redis.get(self._redis_key(key))
        if data:
            parsed = json.loads(data)
            if parsed.get("status") == "PROCESSING":
                return None
            return parsed
        return None
