import asyncio
import json

from workers.services.parsers.twitch_parser import parse_streamers, parse_streams, game_parser, get_token
from workers.services.services import write_streamers_service, write_games_service, write_streams
from workers.config.config import kafka_settings
import logging
from aiokafka import AIOKafkaConsumer


class TwitchConsumer:
    def __init__(self):
        self.logger = logging.getLogger('Twitch Consumer')
        self.bootstrap_servers = kafka_settings.bootstrap_servers,
        self.group_id = kafka_settings.twitch_group_id

    async def consume_parse_streamers(self):
        self.logger.info('parse streamers consumer started')

        consumer = AIOKafkaConsumer(
            'parse_streamers_topic',
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False
        )
        await consumer.start()
        try:
            async for message in consumer:
                data_str = message.value.decode('utf-8')
                data = json.loads(data_str)
                await self.process_streamers(data)
                await consumer.commit()
        finally:
            await consumer.stop()

    async def consume_parse_streams(self):
        self.logger.info('parse streams consumer started')

        consumer = AIOKafkaConsumer(
            'parse_streams_topic',
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False
        )
        await consumer.start()
        try:
            async for message in consumer:
                data_str = message.value.decode('utf-8')
                data = json.loads(data_str)
                await self.process_streams(data)
                await consumer.commit()
        finally:
            await consumer.stop()

    async def consume_parse_games(self):
        self.logger.info('parse games consumer started')

        consumer = AIOKafkaConsumer(
            'parse_games_topic',
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False
        )
        await consumer.start()
        try:
            async for message in consumer:
                data_str = message.value.decode('utf-8')
                data = json.loads(data_str)
                await self.process_games(data)
                await consumer.commit()
        finally:
            await consumer.stop()

    async def process_streamers(self, data):
        streamers_data = await parse_streamers(get_token(), data['streamers'])
        await write_streamers_service(streamers_data)

    async def process_streams(self, data):
        await write_streams(await parse_streams(get_token(), data['params']))

    async def process_games(self, data):
        games_data = await game_parser(get_token(), data['query'])
        await write_games_service(games_data)
