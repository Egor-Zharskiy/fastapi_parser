from typing import Union, List, Optional

from fastapi import APIRouter, status, Query, HTTPException
from fastapi.responses import JSONResponse

from twitch.parser import parse_streamers, parse_streams
from twitch.parser import get_token
from twitch.schemas import Stream, StreamUpdate, StreamersRequest, Streamer
from twitch.services import get_streams_service, delete_stream_service, update_stream_service, create_stream_service, \
    write_streamers_service, get_streamers_service

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
async def parse_streams(query: Optional[str] = None):
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
