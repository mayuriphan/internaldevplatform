import hashlib
import json


class IdempotencyService:

    def __init__(self, redis_client):
        self.redis = redis_client

    def generate_key(self, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def exists(self, key: str) -> bool:
        return self.redis.get(key) is not None

    def store(self, key: str, value: dict, ttl_seconds: int = 3600):
        self.redis.setex(
            key,
            ttl_seconds,
            json.dumps(value),
        )

    def get(self, key: str):
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None