from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Dict

from pydantic import BaseModel, Field


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


class Game(BaseModel):
    id: str
    name: str
    box_art_url: str
    igdb_id: str


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


class Product(BaseModel):
    price: Optional[str]
    product_name: str
    name_model: str
    link: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[str] = None
    description: Dict[str, str] = Field(default_factory=dict)


class SexEnum(Enum):
    man = "man"
    woman = "woman"
    kids = "kids"


class Brand(BaseModel):
    name: str
    url: str
    sex: SexEnum
