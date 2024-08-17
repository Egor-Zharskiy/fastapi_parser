from enum import Enum


class SexEnum(Enum):
    man = "man"
    woman = "woman"
    kids = "kids"


genders = {
    "man": "https://www.lamoda.by/men-home/?sitelink=topmenuM",
    "woman": "https://www.lamoda.by/women-home/?sitelink=topmenuW",
    "kids": "https://www.lamoda.by/kids-home/?sitelink=topmenuK",
}
