from typing import Optional

from pymongo import MongoClient

from config import DB_HOST, DB_PORT, DB_NAME


class MongoConnection:
    def __init__(self):
        self.client = MongoClient(DB_HOST, int(DB_PORT))
        self.db = self.client[DB_NAME]

    def find_data(self, collection: str, query: Optional[dict] = None):
        return self.db[collection].find(query)

    def find_one(self, collection: str, query: Optional[dict] = None):
        return self.db[collection].find_one(query)

    def insert_one(self, collection: str, data: dict):  # insert only one value
        self.db[collection].insert_one(data)

    def insert_data(self, collection: str, data: list):  # insert list of values
        self.db[collection].insert_many(data)

    def update_data(self, collection: str, query: dict, data: dict):
        return self.db[collection].update_one(query, {"$set": data}, upsert=True)

    def insert_or_update_data(self, collection: str, data: dict):
        query = {"product_name": data["product_name"], "name_model": data["name_model"],
                 "description": data["description"]}
        existing_product = self.find_one(collection, query)
        if existing_product:
            self.update_data(collection, query, data)
        else:
            self.insert_one(collection, data)

    def delete_one(self, collection: str, query: dict):
        result = self.db[collection].delete_one(query)
        return result.deleted_count
