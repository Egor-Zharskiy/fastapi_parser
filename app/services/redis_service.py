from typing import Optional

import redis as redis
from app.config.redis_config import redis_settings


class RedisService:
    def __init__(self):
        self.redis = redis.Redis(
            host=redis_settings.host,
            password=redis_settings.password,
            decode_responses=True
        )

    def get_value(self, key: str):
        return self.redis.get(key)

    def set_value(self, key: str, value, ex: Optional[int] = None):
        self.redis.set(key, value, ex)

    def exists(self, key):
        return True if self.redis.exists(key) else False

    def close(self):
        self.redis.close()

    def delete(self, key: str):
        self.redis.delete(key)

    def get_keys(self):
        return self.redis.keys()


redis_client = RedisService()
