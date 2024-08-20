from pymongo import MongoClient
from config import DB_HOST, DB_PORT, DB_NAME

client = MongoClient(DB_HOST, int(DB_PORT))
db = client[DB_NAME]

a = db['streams'].find(None)
print(list(a))
