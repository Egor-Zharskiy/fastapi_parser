from typing import Union, List

import requests
from workers.config.config import twitch_settings
from workers.schemas.schemas import Stream, Streamer, Game
from workers.utils.utils import parse_query
from fastapi import status, HTTPException

from workers.constants.twitch import game_url, stream_url, user_url, token_url


def get_token():
    query = {'client_id': twitch_settings.client_id, "client_secret": twitch_settings.secret_key,
             'grant_type': twitch_settings.credentials}
    response = requests.post(token_url, params=query)

    return response.json()['access_token']


def parse_streamers(token: str, username: Union[str, list]) -> list:
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="List of streamers logins is required")

    url = user_url
    headers = {"Client-ID": twitch_settings.client_id, "Authorization": f"Bearer {token}"}
    params = {
        "login": username
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error while fetching data from Twitch API")

    streamers = [Streamer(**streamer) for streamer in response.json()['data']]

    print(streamers)

    return streamers


def parse_streams(token: str, query: str):
    streams = []
    url = stream_url
    headers = {"Client-ID": twitch_settings.client_id, "Authorization": f"Bearer {token}"}
    params = parse_query(query)

    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']
    if not data:
        print('nothing to save after parsing')  # add logging
        return streams

    for stream in data:
        streams.append(Stream(**stream))

    return streams


def game_parser(token: str, query: str) -> List[Game]:
    url = game_url
    params = parse_query(query)
    headers = {"Client-ID": twitch_settings.client_id, "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        games = [Game(**game) for game in response.json()['data']]
        print(games)
        return games
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                     detail='error with TWITCH API, please verify that query data is correct')
