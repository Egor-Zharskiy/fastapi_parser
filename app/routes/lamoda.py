from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from services.lamoda_producer import LamodaProducer
from schemas.lamoda import Category, Product, SexEnum
from services.lamoda_services import get_cat_names, get_brands_service, write_categories, \
    delete_category_service, create_product_service, update_product_service, delete_item_service, get_url, \
    get_products_by_brand_service

from typing import Dict, List

router = APIRouter(
    prefix='/lamoda',
    tags=["Lamoda"]
)

producer = LamodaProducer()


@router.get('/update_categories_names',
            description='parse Lamoda to update information about categories in the database')
async def update_categories_names(gender: SexEnum):
    producer.send_request('parse_categories_names_topic', gender.value, {"gender": gender.value})
    await write_categories(gender.value)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": "categories successfully updated"})


@router.delete('/delete_category', description='delete category from database')
async def delete_category(gender: SexEnum, category_name: str):
    return await delete_category_service(gender.value, category_name)


@router.get('/get_categories', response_model=Dict[str, Dict[str, List[Category]]])
async def get_categories():
    data = await get_cat_names()
    return {"data": data}


@router.get('/get_brands', description="get brands of gender(values: man, woman, kids or None)")
async def get_brands(sex: SexEnum):
    data = await get_brands_service(sex.value)
    return {"data": data}


@router.get('/parse_brand_items', description="parse brand's items by the name of the brand")
async def get_brand_items(brand: str, gender: SexEnum):
    producer.send_request("parse_brand_topic", brand, {"brand": brand, "gender": gender.value})

    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to Kafka.')


@router.get("/parse_category/", description='get all products from the given category')
async def get_all_prods(sex: SexEnum, category: str):
    url = await get_url(sex.value, category)
    producer.send_request("parse_category_topic", category, {"url": url})

    return JSONResponse(status_code=status.HTTP_200_OK, content='Request sent to Kafka.')


@router.get('/products/', description='get product by brand name')
async def get_products(brand: str):
    data = await get_products_by_brand_service(brand)
    return data


@router.delete('/product')
async def delete_item(item_id: str):
    return await delete_item_service(item_id)


@router.post('/product')
async def create_product(product: Product):
    return await create_product_service(product)


@router.put('/product/{product_id}')
async def update_product(product_id: str, data: Product):
    return await update_product_service(product_id, data)
