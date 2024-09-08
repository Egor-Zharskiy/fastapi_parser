import json

from workers.services.services import write_items_service, get_category_products, get_brand_url, write_categories
from workers.config.config import kafka_settings
import logging
from aiokafka import AIOKafkaConsumer


class LamodaConsumer:
    def __init__(self):
        self.logger = logging.getLogger('Lamoda Consumer')
        self.bootstrap_servers = kafka_settings.bootstrap_servers
        self.group_id = kafka_settings.kafka_group_id

    async def consume_parse_category(self):
        self.logger.info('Starting category parser consumer')

        consumer = AIOKafkaConsumer(
            'parse_category_topic',
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False
        )
        await consumer.start()
        try:
            async for message in consumer:
                data_str = message.value.decode('utf-8')
                data = json.loads(data_str)
                await self.process_categories_items(data)
        finally:
            await consumer.stop()

    async def consume_parse_brands(self):
        self.logger.info('brand parser consumer')

        consumer = AIOKafkaConsumer(
            'parse_brand_topic',
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            max_poll_interval_ms=600000,
            session_timeout_ms=30000,
            enable_auto_commit=False

        )
        await consumer.start()
        try:
            async for message in consumer:
                data_str = message.value.decode('utf-8')
                data = json.loads(data_str)
                await self.process_brands(data)
                await consumer.commit()
        finally:
            await consumer.stop()

    async def consume_parse_categories(self):
        self.logger.info('categories names consumer')
        print('categories names consumer')

        consumer = AIOKafkaConsumer(
            'parse_categories_names_topic',
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            max_poll_interval_ms=600000,
            session_timeout_ms=30000,
            enable_auto_commit=False

        )
        await consumer.start()
        try:
            async for message in consumer:
                data_str = message.value.decode('utf-8')
                data = json.loads(data_str)
                await self.process_categories(data)
                await consumer.commit()
        finally:
            await consumer.stop()

    async def process_categories_items(self, data):
        products_data = await get_category_products(data['url'])
        await write_items_service(products_data)

    async def process_brands(self, data):
        brand_url = await get_brand_url(data['gender'], data['brand'])
        products = await get_category_products(brand_url)
        await write_items_service(products)

    async def process_categories(self, data):
        await write_categories(data['gender'])
