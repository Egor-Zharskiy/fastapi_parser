from typing import Union

import requests
from config import CLIENT_ID, SECRET_KEY, CREDENTIALS
from twitch.schemas import Stream, Streamer
from twitch.services import write_streams
from twitch.utils import parse_query
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

from constants import game_url, stream_url, user_url, token_url


def get_token():
    query = {'client_id': CLIENT_ID, "client_secret": SECRET_KEY, 'grant_type': CREDENTIALS}
    response = requests.post(token_url, params=query)

    return response.json()['access_token']


def parse_streamers(token: str, username: Union[str, list]) -> list:
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="List of streamers logins is required")

    url = user_url
    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {token}"}
    params = {
        "login": username
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error while fetching data from Twitch API")

    streamers = [Streamer(**streamer) for streamer in response.json()['data']]
    return streamers


def parse_streams(token: str, query: str):
    streams = []
    url = stream_url
    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {token}"}
    params = parse_query(query)

    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']
    for stream in data:
        streams.append(Stream(**stream))

    write_streams(streams)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Parsed successfully")


def parse_games(token: str, query: str):
    url = game_url
