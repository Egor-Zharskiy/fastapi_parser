from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from lamoda.constants import SexEnum
from lamoda.schemas import Category, Product
from lamoda.services import get_cat_names, get_url, get_brands_service, get_brand_url, write_categories, \
    delete_category_service, write_items_service, create_product_service, update_product_service, delete_item_service

from typing import Dict, List

from lamoda.parser import get_category_products, get_detailed_product

router = APIRouter(
    prefix='/lamoda',
    tags=["Lamoda"]
)


@router.get('/update_categories_names',
            description='parse Lamoda to update information about categories in the database')
async def update_categories_names(gender: SexEnum):
    write_categories(gender.value)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": "categories successfully updated"})


@router.delete('/delete_category', description='delete category from database')
async def delete_category(gender: SexEnum, category_name: str):
    return delete_category_service(gender.value, category_name)


@router.get('/get_categories', response_model=Dict[str, Dict[str, List[Category]]])
async def get_categories():
    data = await get_cat_names()
    return {"data": data}


@router.get('/get_brands', description="get brands of gender(values: man, woman, kids or None)")
async def get_brands(sex: SexEnum):
    data = await get_brands_service(sex.value)
    return {"data": data}


@router.get('/get_brand_items', description="get brand's items by the name of the brand")
async def get_brand_items(brand: str, gender: SexEnum):
    brand_url = await get_brand_url(gender.value, brand)
    products = await get_category_products(brand_url)
    write_items_service(products)
    return {"data": products}


@router.get("/product/{url}/", response_model=Dict[str, Product], description="get full information about item")
async def get_product(url: str):
    data = await get_detailed_product(url)
    return {"data": data}


@router.get("/category/")
async def get_all_prods(sex: SexEnum, category: str):
    url = await get_url(sex.value, category)
    products = await get_category_products(url)
    write_items_service(products)
    return {"data": products}


@router.delete('/product')
async def delete_item(item_id: str):
    return delete_item_service(item_id)


@router.post('/product')
async def create_product(product: Product):
    return create_product_service(product)


@router.put('/product/{product_id}')
async def update_product(product_id: str, data: Product):
    return update_product_service(product_id, data)
