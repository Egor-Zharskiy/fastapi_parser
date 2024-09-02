from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from services.twitch_producer import TwitchProducer
from workers.services.parsers.twitch_parser import parse_streamers
from workers.services.parsers.twitch_parser import get_token
from schemas.twitch import Stream, StreamUpdate, StreamersRequest, Game, GameUpdate
from services.twitch_services import get_streams_service, delete_stream_service, update_stream_service, create_stream_service, \
    get_streamers_service, save_game, update_game_service, \
    delete_game_service

router = APIRouter(
    prefix='/twitch',
    tags=["Twitch"]
)

producer = TwitchProducer()


@router.post('/parse_streamers', description='get the list of the streamers by given list of logins')
async def get_streamers(streamers: StreamersRequest):
    producer.send_streamers_request(streamers.list_of_streamers)

    # streamers_data = parse_streamers(get_token(), streamers.list_of_streamers)
    # write_streamers_service(streamers_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to kafka')


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
async def streams_parser(request: Request):
    producer.send_streams_request(str(request.query_params))
    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to kafka')
    # return parse_streams(get_token(), str(request.query_params))


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
async def parse_games(request: Request):
    # data = game_parser(get_token(), str(request.query_params))
    # return write_games_service(data)

    producer.send_games_request(str(request.query_params))
    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to kafka')


@router.post('/game', description="save information about game into db")
async def create_game(game: Game):
    return save_game(game)


@router.patch('/game', description="update information about game")
async def update_game(game_id: str, game: GameUpdate):
    return update_game_service(game_id, game)


@router.delete('/game')
async def delete_game(game_id: str):
    return delete_game_service(game_id)
