from fastapi import FastAPI

from app.config.error_controller import error_controller
from app.routes.lamoda import router as lamoda_router
from app.routes.twitch import router as twitch_router
from app.config.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(lamoda_router)
app.include_router(twitch_router)

app.add_exception_handler(ValueError, error_controller)
