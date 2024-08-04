from fastapi import APIRouter

from lamoda.services import get_products_from_page, get_all_products_from

import time

router = APIRouter(
    prefix='/lamoda',
    tags=["Lamoda"]
)


@router.get("/get_one_page_products")
async def hello(url: str):
    start_time = time.time()
    data = await get_products_from_page(url)
    end_time = time.time()
    execution_time = end_time - start_time  # вычисляем время выполнения
    print(execution_time)
    quantity = len(data)
    return {
        "data": data,
        "quantity": quantity
    }


@router.get("/get_all_products_from_category")
def get_all_prods(url: str):
    products = get_all_products_from(url)
    return {
        "data":
            products
    }
