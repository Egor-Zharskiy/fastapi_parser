from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('DB_HOST'), int(os.getenv('DB_PORT')))
db = client[os.getenv('DB_NAME')]
