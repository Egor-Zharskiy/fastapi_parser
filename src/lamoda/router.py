from fastapi import APIRouter

from lamoda.schemas import Category
from lamoda.services import get_cat_names, get_url, get_brands_service, get_brand_url

from typing import Dict, List, Optional

from lamoda.parser import get_all_products_from, get_detailed_product

router = APIRouter(
    prefix='/lamoda',
    tags=["Lamoda"]
)


@router.get('/get_categories_names', response_model=Dict[str, Dict[str, List[Category]]])
async def get_categories():
    data = await get_cat_names()
    return {"data": data}


@router.get('/get_brands', description="get brands of gender(values: man, woman, kids or None)")
async def get_brands(sex: Optional[str] = None):
    data = await get_brands_service(sex)
    return {"data": data}


@router.get('/get_brand_items', description="get brand's items by the name of the brand")
async def get_brand_items(brand: str, gender: str):
    brand_url = await get_brand_url(gender, brand)

    products = await get_all_products_from(brand_url)
    return {"data": products}


@router.get("/get_info_from_product", response_model=Dict[str, Dict])
async def get_product(url: str):
    data = await get_detailed_product(url)
    return {"data": data}


@router.get("/get_all_products_from_category")
async def get_all_prods(sex: str, category: str):
    url = await get_url(sex, category)
    products = await get_all_products_from(url)
    return {"data": products}
