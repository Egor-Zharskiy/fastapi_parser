from confluent_kafka import Producer, Consumer, KafkaError
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


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, topic: str):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([topic])

    def consume_messages(self, process_function):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break
            data = json.loads(msg.value().decode('utf-8'))
            process_function(data)

    def close(self):
        self.consumer.close()
