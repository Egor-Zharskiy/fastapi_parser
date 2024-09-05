from app.config.config import kafka_settings
from config.kafka import KafkaProducer


class TwitchProducer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=kafka_settings.bootstrap_servers,
                                      client_id=kafka_settings.client_id)

    def send_streamers_request(self, streamers: list):
        self.producer.send_message('parse_streamers_topic', 'streamers', {'streamers': streamers})

    def send_streams_request(self, params: str):
        self.producer.send_message('parse_streams_topic', 'streams', {'params': params})

    def send_games_request(self, query: str):
        self.producer.send_message('parse_games_topic', 'games', {'query': query})
