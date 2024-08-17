from typing import Dict, List, Optional, Union
from datetime import datetime

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from database import MongoConnection
from lamoda import constants
from lamoda.constants import SexEnum
from lamoda.parser import parse_categories
from lamoda.schemas import Category, Brand


async def get_categories_service() -> list:
    db = MongoConnection()
    raw_data = db.find_data('categories')
    categories = []
    for data in raw_data:
        try:
            category = Category(**data)
            categories.append(category)
        except Exception as e:
            print(e)

    return categories


async def get_cat_names() -> Dict[str, List[Category]]:
    data = await get_categories_service()
    cat_names = {'man': [], 'woman': [], 'kids': []}
    for el in data:
        cat_names[el.sex.value].append(el)
    return cat_names


async def get_url(sex: str, category: str):
    data = await get_cat_names()

    if sex not in data.keys():
        raise HTTPException(status_code=404, detail="URL not found")

    for el in data[sex]:
        if el.name.lower() == category.lower():
            return f"https://lamoda.by{el.url}"
    raise HTTPException(status_code=404, detail="URL not found")


async def get_brands_service(gender: Optional[str] = None) -> Optional[Union[list, Exception]]:
    brands = []
    db = MongoConnection()
    raw_data = db.find_data('brands', None if not gender else {"sex": get_gender(gender)})

    try:
        for brand in raw_data:
            brands.append(Brand(**brand))
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return brands


async def get_brand_url(gender: str, brand_name: str) -> Union[str, Exception]:
    db = MongoConnection()
    try:
        raw_data = db.find_one('brands', {"sex": gender, "name": brand_name.lower()})
        brand = Brand(**raw_data)

    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid data sent to server.')

    return f'https://lamoda.by{brand.url}'


def get_gender(gender: str):
    try:
        return SexEnum(gender).value
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect gender: available: man, woman, kids")


def write_categories(gender: str):
    db = MongoConnection()
    try:
        data = parse_categories(constants.genders[gender])
        for item in data:
            query = {"name": item["name"], "sex": gender}
            db.update_data("categories", query, {**item, "sex": gender, "created_at": datetime.now()})
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"ValueError: {str(ve)}")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")


def delete_category_service(gender: str, name: str):
    db = MongoConnection()
    deleted = db.delete_one('categories', {"name": name, "sex": gender})
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content='deleted successfully')
