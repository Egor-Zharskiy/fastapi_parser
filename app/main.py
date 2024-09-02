from fastapi import FastAPI

from config.error_controller import error_controller
from workers.services.lamoda_consumer import LamodaConsumer
from routes.lamoda import router as lamoda_router
from routes.twitch import router as twitch_router
from config.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(lamoda_router)
app.include_router(twitch_router)

app.add_exception_handler(ValueError, error_controller)

if __name__ == "__main__":
    lamoda_consumer = LamodaConsumer()
    # lamoda_consumer.consume_parse_category()
    lamoda_consumer.consume_parse_brands()
    # consumer = TwitchConsumer()
    # consumer.consume_parse_streamers()
    # consumer.consume_parse_streams()
    # consumer.consume_parse_games()
