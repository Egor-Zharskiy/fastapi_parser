from fastapi import FastAPI

from common.error_controller import error_controller
from lamoda.router import router as lamoda_router
from twitch.router import router as twitch_router
from config import AppSettings as settings

app = FastAPI(title=settings().app_name)

app.include_router(lamoda_router)
app.include_router(twitch_router)

app.add_exception_handler(ValueError, error_controller)
