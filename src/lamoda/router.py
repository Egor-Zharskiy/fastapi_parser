from fastapi import APIRouter

from lamoda.schemas import Category
from lamoda.services import get_all_products_from, get_cat_names, get_detailed_product, get_url

from typing import Dict, List

router = APIRouter(
    prefix='/lamoda',
    tags=["Lamoda"]
)


@router.get('/get_categories_names', response_model=Dict[str, List[Category]])
async def get_categories():
    data = await get_cat_names()
    return data


@router.get("/get_info_from_product", response_model=Dict[str, Dict])
async def get_product(url: str):
    data = await get_detailed_product(url)
    return {"data": data}


@router.get("/get_all_products_from_category")
async def get_all_prods(sex: str, category: str):
    url = await get_url(sex, category)
    products = await get_all_products_from(url)
    return {"data": products}
