from common.kafka import KafkaProducer, KafkaConsumer
from twitch.parser import parse_streamers, parse_streams, game_parser, get_token
from twitch.services import write_streamers_service, write_games_service, write_streams


class TwitchProducer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', client_id='twitch-producer')

    def send_streamers_request(self, streamers: list):
        self.producer.send_message('parse_streamers_topic', 'streamers', {'streamers': streamers})

    def send_streams_request(self, params: str):
        self.producer.send_message('parse_streams_topic', 'streams', {'params': params})

    def send_games_request(self, query: str):
        self.producer.send_message('parse_games_topic', 'games', {'query': query})


class TwitchConsumer:
    def __init__(self):
        print('started')
        self.consumer_conf = {
            'bootstrap_servers': 'localhost:9092',
            'group_id': 'twitch-consumer-group'
        }

    def consume_parse_streamers(self):
        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_streamers_topic'
        )
        consumer.consume_messages(self.process_streamers)
        consumer.close()

    def consume_parse_streams(self):
        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_streams_topic'
        )
        consumer.consume_messages(self.process_streams)
        consumer.close()

    def consume_parse_games(self):
        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_games_topic'
        )
        consumer.consume_messages(self.process_games)
        consumer.close()

    def process_streamers(self, data):
        streamers_data = parse_streamers(get_token(), data['streamers'])
        write_streamers_service(streamers_data)

    def process_streams(self, data):
        write_streams(parse_streams(get_token(), data['params']))

    def process_games(self, data):
        games_data = game_parser(get_token(), data['query'])
        write_games_service(games_data)
