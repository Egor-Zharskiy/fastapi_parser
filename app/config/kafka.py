from confluent_kafka import Producer
import json


class KafkaProducer:
    def __init__(self, bootstrap_servers: str, client_id: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'client.id': client_id
        })

    def send_message(self, topic: str, key: str, value: dict):
        self.producer.produce(topic, key=key, value=json.dumps(value))
        self.producer.flush()
