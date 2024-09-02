from workers.config.kafka import KafkaConsumer
from workers.services.services import write_items_service, get_category_products, get_brand_url
from workers.config.config import kafka_settings


class LamodaConsumer:
    def __init__(self):
        print('lamoda consumer started')
        self.consumer_conf = {
            'bootstrap_servers': kafka_settings.bootstrap_servers,
            'group_id': kafka_settings.kafka_group_id
        }

    def consume_parse_category(self):
        print('parse category consumer')
        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_category_topic'
        )
        consumer.consume_messages(self.process_categories)
        consumer.close()

    def consume_parse_brands(self):
        print('brand parser consumer')
        consumer = KafkaConsumer(
            bootstrap_servers=self.consumer_conf['bootstrap_servers'],
            group_id=self.consumer_conf['group_id'],
            topic='parse_brand_topic'
        )
        consumer.consume_messages(self.process_brands)
        consumer.close()

    def process_categories(self, data):
        print(data)

        products_data = get_category_products(data['url'])
        write_items_service(products_data)

    def process_brands(self, data):
        print('processing brand')
        brand_url = get_brand_url(data['gender'], data['brand'])
        products = get_category_products(brand_url)
        write_items_service(products)
