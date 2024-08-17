from datetime import datetime
from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel, Field


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


class Product(BaseModel):
    price: Optional[str]
    product_name: str
    name_model: str
    rating: Optional[float]
    rating_count: Optional[str]
    description: Dict[str, str] = Field(default_factory=dict)
