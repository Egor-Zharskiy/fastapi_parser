from typing import List, Union

from pymongo.errors import DuplicateKeyError

from database import MongoConnection
from twitch.schemas import Stream, StreamUpdate, Streamer, Game
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

db = MongoConnection()


def write_streams(data: List[Stream]):
    for item in data:
        stream = item.to_dict()
        db.insert_or_update_data('streams', stream, {"id": stream['id']})


def get_streams_service() -> dict:
    data = [Stream(**stream) for stream in db.find_data('streams', None)]
    return {"data": data}


def delete_stream_service(stream_id: str) -> JSONResponse:
    result = db.delete_one('streams', {'id': stream_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content='deleted successfully') if result else JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content='Stream not found')


def update_stream_service(stream_id: str, stream: StreamUpdate) -> Union[Stream, JSONResponse]:
    result = db.update_without_create('streams', {"id": stream_id}, stream.to_dict())
    if result.matched_count:
        return Stream(**db.find_one('streams', {'id': stream_id}))
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Stream not found')


def create_stream_service(stream: Stream):
    try:
        db.insert_one('streams', stream.to_dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content='created successfully')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate of unique field")


def write_streamers_service(streamers: Union[List[Streamer], Streamer]):
    try:
        for streamer in streamers:
            db.insert_or_update_data('streamers', streamer.dict(), {"id": streamer.id})
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Streamer with this id already exists.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="an unexpected error occurred")


def get_streamers_service(logins: List[str]):
    query = {"login": {"$in": logins}}
    streamers_data = db.find_data('streamers', query)
    return [Streamer(**streamer) for streamer in streamers_data]


def write_games_service(data: List[Game]):
    try:
        for item in data:
            game = item.dict()
            db.insert_or_update_data('games', game, {"id": game["id"]})

    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Duplicate of unique key error")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="an unexpected error occurred")

    return JSONResponse(status_code=status.HTTP_200_OK, content='Parsed successfully')
