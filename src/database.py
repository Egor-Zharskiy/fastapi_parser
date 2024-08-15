from typing import Optional

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class MongoConnection:
    def __init__(self):
        self.client = MongoClient(os.getenv('DB_HOST'), int(os.getenv('DB_PORT')))
        self.db = self.client[os.getenv('DB_NAME')]

    def find_data(self, collection: str, query: Optional[dict] = None):
        return self.db[collection].find(query)

    def find_one(self, collection: str, query: Optional[dict] = None):
        return self.db[collection].find_one(query)

    def insert_data(self, collection: str, data: dict):
        self.db[collection].insert_one(data)
