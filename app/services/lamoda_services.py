import json
from typing import Dict, List, Optional, Union
from bson import ObjectId

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.database import MongoConnection
from app.services.redis_service import redis_client
from app.schemas.lamoda import Category, Brand, Product, SexEnum

import logging

logger = logging.getLogger('Lamoda Services')
db = MongoConnection()


async def get_categories_service() -> list:
    raw_data = db.find_data('categories')
    categories = []
    for data in raw_data:
        try:
            category = Category(**data)
            print(category)
            categories.append(category)
        except Exception as e:
            print("ERROR!!!")
            print(str(e))
            logger.error(str(e))
    print(categories, 'categories123123')
    return categories


async def get_cat_names() -> Dict[str, List[Category]]:
    print('getting categories names')
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
    raw_data = db.find_data('brands', None if not gender else {"sex": get_gender(gender)})

    try:
        for brand in raw_data:
            brands.append(Brand(**brand))
    except Exception as e:
        logger.error(str(e))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return brands


async def get_brand_url(gender: str, brand_name: str) -> Union[str, Exception]:
    try:

        raw_data = db.find_one('brands', {"sex": gender, "name": brand_name.lower()})
        brand = Brand(**raw_data)
        return f'https://lamoda.by{brand.url}'


    except TypeError as e:
        logger.error(str(e))



def get_gender(gender: str):
    try:
        return SexEnum(gender).value
    except TypeError as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect gender: available: man, woman, kids")


# async def write_categories(gender: str):
#     try:
#         data = await parse_categories(genders[gender])
#         for item in data:
#             query = {"name": item["name"], "sex": gender}
#             db.update_data("categories", query, {**item, "sex": gender, "created_at": datetime.now()})
#     except TypeError as te:
#         logger.error(str(te))
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"TypeError: {str(te)}")
#
#     except Exception as e:
#         logger.error(str(e))
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail=f"An unexpected error occurred: {str(e)}")


async def delete_category_service(gender: str, name: str):
    deleted = db.delete_one('categories', {"name": name, "sex": gender})
    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content='deleted successfully')


def write_items_service(data: List[Product]):
    try:
        for item in data:
            product = item.dict()
            db.insert_or_update_data('items', product,
                                     {"product_name": product["product_name"],
                                      "name_model": product["name_model"].lower(),
                                      "description": product["description"]})
    except Exception as e:
        logger.error(f"Unexpected error occurred {str(e)}")


async def create_product_service(product: Product):
    db.insert_one('items', product.dict())
    return JSONResponse(status_code=status.HTTP_200_OK, content="Product created")


async def update_product_service(product_id: str, data: Product):
    product_data = data.dict()

    object_id = ObjectId(product_id)

    db.update_data('items', {"_id": object_id}, product_data)

    return JSONResponse(status_code=status.HTTP_200_OK, content="Product updated successfully")


async def delete_item_service(product_id: str):
    db.delete_one('items', {"_id": product_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content="deleted successfully")


async def get_products_by_brand_service(brand: str) -> list:
    redis_data = redis_client.get_value(f"{brand} items")
    if redis_data:
        logger.info('data from redis')
        raw_data = json.loads(redis_data)
        data = [Product(**product) for product in raw_data]
    else:
        logger.info('data from db')
        raw_data = list(db.find_data('items', {"name_model": brand}))
        data = [Product(**product) for product in raw_data]
        redis_client.set_value(f"{brand} items", json.dumps([product.dict() for product in data]), ex=300)

    return data
