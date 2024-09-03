from workers.config.config import kafka_settings
from workers.config.kafka import KafkaProducer
import logging


class LamodaProducer:
    def __init__(self):
        self.logger = logging.getLogger('Lamoda Producer')

        self.producer = KafkaProducer(bootstrap_servers=kafka_settings.bootstrap_servers,
                                      client_id=kafka_settings.client_id)

    def send_category_request(self, category_url: str, category_name: str):
        message = {
            "url": category_url,
            "category": category_name
        }

        self.producer.send_message("parse_category_topic", category_name, {"message": message})
        self.logger.info('parse category message sent')

    def send_request(self, topic: str, key: str, data: dict):
        self.logger.info("topic", topic, data)
        self.producer.send_message(topic, key, data)
