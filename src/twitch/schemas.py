from datetime import datetime
from typing import Union, Optional, List, Literal

from pydantic import BaseModel
from enum import Enum


class Type(Enum):
    live = 'live'
    all = 'all'


class Stream(BaseModel):
    id: str
    user_id: str
    user_login: str
    user_name: str
    game_id: str
    game_name: str
    type: Type
    title: str
    viewer_count: int
    started_at: datetime
    language: str
    tags: list
    is_mature: bool
    added_to_db: datetime = datetime.now()

    def to_dict(self) -> dict:
        data = self.dict()
        data['type'] = self.type.value
        return data


class StreamUpdate(BaseModel):
    user_id: Optional[str] = None
    user_login: Optional[str] = None
    user_name: Optional[str] = None
    game_id: Optional[str] = None
    game_name: Optional[str] = None
    type: Optional[Type] = None
    title: Optional[str] = None
    viewer_count: Optional[int] = None
    started_at: Optional[datetime] = None
    language: Optional[str] = None
    tags: Optional[list] = None
    is_mature: Optional[bool] = None

    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        if data.get('type'):
            data['type'] = self.type.value
        return data


class Streamer(BaseModel):
    id: str
    login: str
    display_name: str
    type: Literal["admin", "global_mod", "staff", ""]
    broadcaster_type: Literal["affiliate", "partner", ""]
    description: str
    profile_image_url: str
    offline_image_url: str
    view_count: int
    created_at: datetime


class StreamersRequest(BaseModel):
    list_of_streamers: List[str]
