from typing import Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from twitch.parser import parse_streamers, parse_streams, game_parser
from twitch.parser import get_token
from twitch.schemas import Stream, StreamUpdate, StreamersRequest, Streamer, Game, GameUpdate
from twitch.services import get_streams_service, delete_stream_service, update_stream_service, create_stream_service, \
    write_streamers_service, get_streamers_service, write_games_service, save_game, update_game_service, \
    delete_game_service

router = APIRouter(
    prefix='/twitch',
    tags=["Twitch"]
)


@router.post('/parse_streamers', description='get the list of the streamers by given list of logins')
async def get_streamers(streamers: StreamersRequest):
    streamers_data = parse_streamers(get_token(), streamers.list_of_streamers)
    write_streamers_service(streamers_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content='data saved successfully')


@router.get('/streamer/{username}', description='get information about streamer by his username')
async def get_streamer(username: str):
    return parse_streamers(get_token(), username)


@router.post('/get_list_of_streamers',
             description='get information about streamers whose logins are sent in the request')
async def get_list_of_streamers(streamers: StreamersRequest):
    return get_streamers_service(streamers.list_of_streamers)


@router.get('/parse_streams',
            description="Get streams with parameters: user_login, user_id, language, game_id, type."
                        "Query example: &user_id=123&user_login=buster")
async def streams_parser(query: Optional[str] = None):
    return parse_streams(get_token(), query)


@router.get('/streams', description='get all saved to db streams')
async def get_streams():
    return get_streams_service()


@router.delete('/streams', description='delete existing stream')
async def delete_stream(stream_id: str):
    return delete_stream_service(stream_id)


@router.patch('/streams', description='update existing stream information in db')
async def update_stream(stream_id: str, stream: StreamUpdate):
    return update_stream_service(stream_id, stream)


@router.post('/streams', description='create stream and insert into db')
async def create_stream(stream: Stream):
    return create_stream_service(stream)


@router.get('/parse_games')
async def parse_games(query: Optional[str] = None):
    data = game_parser(get_token(), query)
    return write_games_service(data)


@router.post('/game', description="save information about game into db")
async def create_game(game: Game):
    return save_game(game)


@router.patch('/game', description="update information about game")
async def update_game(game_id: str, game: GameUpdate):
    return update_game_service(game_id, game)


@router.delete('/game')
async def delete_game(game_id: str):
    return delete_game_service(game_id)
