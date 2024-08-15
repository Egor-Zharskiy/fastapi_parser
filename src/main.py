from fastapi import FastAPI
from lamoda.router import router as lamoda_router

app = FastAPI(
    title="Lamoda+Twitch Parser"
)

app.include_router(lamoda_router)
