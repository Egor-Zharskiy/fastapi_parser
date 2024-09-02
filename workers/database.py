from typing import Optional

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from app.config.config import settings


class MongoConnection:
    def __init__(self):
        self.client = MongoClient(settings.db_host, int(settings.db_port))
        self.db = self.client[settings.db_name]

    def create_stream_indexes(self):
        self.db['streams'].create_index("id", unique=True)

    def create_streamer_indexes(self):
        self.db['streamers'].create_index("id", unique=True)

    def create_game_indexes(self):
        self.db['games'].create_index("id", unique=True)

    def find_data(self, collection: str, query: Optional[dict] = None):
        return self.db[collection].find(query)

    def find_one(self, collection: str, query: Optional[dict] = None):
        return self.db[collection].find_one(query)

    def insert_one(self, collection: str, data: dict):  # insert only one value
        try:
            self.db[collection].insert_one(data)
        except DuplicateKeyError:
            raise ValueError('Duplicate unique key error')

    def insert_data(self, collection: str, data: list):  # insert list of values
        try:
            self.db[collection].insert_many(data)
        except DuplicateKeyError:
            raise ValueError('Duplicate unique key error')

    def update_data(self, collection: str, query: dict, data: dict):
        try:
            return self.db[collection].update_one(query, {"$set": data}, upsert=True)
        except DuplicateKeyError:
            raise ValueError('Duplicate unique key error')

    def update_without_create(self, collection: str, query: dict, data: dict):
        try:
            return self.db[collection].update_one(query, {"$set": data}, upsert=False)
        except DuplicateKeyError:
            raise ValueError('Duplicate unique key error')

    def insert_or_update_data(self, collection: str, data: dict, query: dict):
        try:
            existing_product = self.find_one(collection, query)
            if existing_product:
                self.update_data(collection, query, data)
            else:
                self.insert_one(collection, data)
        except DuplicateKeyError:
            raise ValueError('Duplicate unique key error')

    def delete_one(self, collection: str, query: dict):
        result = self.db[collection].delete_one(query)
        return result.deleted_count
