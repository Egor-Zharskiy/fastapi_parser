import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class RedisSettings(BaseSettings):
    host: str = os.getenv("REDIS_HOST")
    port: str = os.getenv("REDIS_PORT")
    username: str = os.getenv("REDIS_USER")
    password: str = os.getenv("REDIS_USER_PASSWORD")


redis_settings = RedisSettings()
