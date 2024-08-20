from fastapi import FastAPI
from lamoda.router import router as lamoda_router
from twitch.router import router as twitch_router

app = FastAPI(
    title="Lamoda+Twitch Parser"
)

app.include_router(lamoda_router)
app.include_router(twitch_router)
