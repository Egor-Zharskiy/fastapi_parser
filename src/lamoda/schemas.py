from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class SexEnum(Enum):
    man = "man"
    woman = "woman"
    kids = "kids"


class Category(BaseModel):
    name: str
    url: str
    created_at: datetime
    sex: SexEnum


class Brand(BaseModel):
    name: str
    url: str
    sex: SexEnum
