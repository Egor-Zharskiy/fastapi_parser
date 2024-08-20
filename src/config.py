import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SECRET_KEY = os.getenv('TWITCH_SECRET_KEY')
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CREDENTIALS = os.getenv('TWITCH_GRANT_TYPE')
