from workers.config.kafka import KafkaConsumer
from workers.services.parsers.twitch_parser import parse_streamers, parse_streams, game_parser, get_token
from workers.services.services import write_streamers_service, write_games_service, write_streams
from workers.config.config import kafka_settings
import logging


class TwitchConsumer:
    def __init__(self):
        self.logger = logging.getLogger('Twitch Consumer')
        self.logger.setLevel(logging.ERROR)
        self.consumer_conf = {
            'bootstrap_servers': kafka_settings.bootstrap_servers,
            'group_id': kafka_settings.twitch_group_id
        }

    def consume_parse_streamers(self):
        self.logger.info('parse streamers consumer started')

        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_streamers_topic'
        )
        consumer.consume_messages(self.process_streamers)
        consumer.close()

    def consume_parse_streams(self):
        self.logger.info('parse streams consumer started')

        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_streams_topic'
        )
        consumer.consume_messages(self.process_streams)
        consumer.close()

    def consume_parse_games(self):
        self.logger.info('parse games consumer started')

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
