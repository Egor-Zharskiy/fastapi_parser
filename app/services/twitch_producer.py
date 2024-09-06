from app.config.config import kafka_settings
from config.kafka import KafkaProducer
import logging


class TwitchProducer:
    def __init__(self):
        self.logger = logging.getLogger('Twitch Producer')

        self.producer = KafkaProducer(bootstrap_servers=kafka_settings.bootstrap_servers,
                                      client_id=kafka_settings.client_id)

    def send_request(self, topic: str, key: str, data: dict):
        self.logger.info("topic", topic, data)
        self.producer.send_message(topic, key, data)
