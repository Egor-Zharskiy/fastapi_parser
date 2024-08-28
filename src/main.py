from fastapi import FastAPI

from common.error_controller import error_controller
from lamoda.router import router as lamoda_router
from twitch.kafka_service import TwitchConsumer
from twitch.router import router as twitch_router
from config import settings

app = FastAPI(title=settings.app_name)

app.include_router(lamoda_router)
app.include_router(twitch_router)

app.add_exception_handler(ValueError, error_controller)

if __name__ == "__main__":
    consumer = TwitchConsumer()
    # consumer.consume_parse_streamers()
    consumer.consume_parse_streams()
    # consumer.consume_parse_games()
