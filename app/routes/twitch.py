from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from app.services.twitch_producer import TwitchProducer
from app.schemas.twitch import Stream, StreamUpdate, StreamersRequest, Game, GameUpdate
from app.services.twitch_services import get_streams_service, delete_stream_service, update_stream_service, \
    create_stream_service, \
    get_streamers_service, save_game, update_game_service, \
    delete_game_service, get_streamer_service

router = APIRouter(
    prefix='/twitch',
    tags=["Twitch"]
)

producer = TwitchProducer()


@router.post('/parse_streamers', description='get the list of the streamers by given list of logins')
async def get_streamers(streamers: StreamersRequest):
    producer.send_request('parse_streamers_topic', 'streamers',
                          {"streamers": streamers.list_of_streamers})
    # producer.send_streamers_request(streamers.list_of_streamers)

    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to kafka')


@router.get('/streamer/{username}', description='get information about streamer by his username')
async def get_streamer(username: str):
    return await get_streamer_service(username)


@router.post('/get_list_of_streamers',
             description='get information about streamers whose logins are sent in the request')
async def get_list_of_streamers(streamers: StreamersRequest):
    return get_streamers_service(streamers.list_of_streamers)


@router.get('/parse_streams',
            description="Get streams with parameters: user_login, user_id, language, game_id, type."
                        "Query example: user_id=123&user_login=buster")
async def streams_parser(request: Request):
    producer.send_request('parse_streams_topic', 'streams', {"params": str(request.query_params)})
    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to kafka')


@router.get('/streams', description='get all saved to db streams')
async def get_streams():
    return await get_streams_service()


@router.delete('/streams', description='delete existing stream')
async def delete_stream(stream_id: str):
    return await delete_stream_service(stream_id)


@router.patch('/streams', description='update existing stream information in db')
async def update_stream(stream_id: str, stream: StreamUpdate):
    return await update_stream_service(stream_id, stream)


@router.post('/streams', description='create stream and insert into db')
async def create_stream(stream: Stream):
    return await create_stream_service(stream)


@router.get('/parse_games', description='parse games by game id, name and igdb_id')
async def parse_games(request: Request):
    producer.send_request('parse_games_topic', str(request.query_params), {"query": str(request.query_params)})
    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to kafka')


@router.post('/game', description="save information about game into db")
async def create_game(game: Game):
    return await save_game(game)


@router.patch('/game', description="update information about game")
async def update_game(game_id: str, game: GameUpdate):
    return await update_game_service(game_id, game)


@router.delete('/game')
async def delete_game(game_id: str):
    return await delete_game_service(game_id)
