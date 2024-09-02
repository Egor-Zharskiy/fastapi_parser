import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class KafkaSettings(BaseSettings):
    client_id: str = os.getenv('KAFKA_CLIENT_ID')
    bootstrap_servers: str = os.getenv("BOOTSTRAP_SERVERS")
    twitch_group_id: str = os.getenv('KAFKA_TWITCH_GROUP_ID')
    kafka_group_id: str = os.getenv('KAFKA_LAMODA_GROUP_ID')


class TwitchSettings(BaseSettings):
    secret_key: str = os.getenv('TWITCH_SECRET_KEY')
    client_id: str = os.getenv('TWITCH_CLIENT_ID')
    credentials: str = os.getenv('TWITCH_GRANT_TYPE')


twitch_settings = TwitchSettings()
kafka_settings = KafkaSettings()
