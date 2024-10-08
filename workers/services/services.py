from cgi import parse
from datetime import datetime
from typing import List, Union

import aiohttp
import bs4.element
import requests
from bs4 import BeautifulSoup

from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import ValidationError

from workers.database import MongoConnection
from workers.schemas.schemas import Product, Brand
from workers.schemas.schemas import Streamer, Game, Stream
from workers.services.parsers.lamoda_parser import generate_next_page_url, parse_categories, parse_brands
from workers.utils.utils import validate_price
from workers.constants.lamoda import genders
import logging

db = MongoConnection()
logger = logging.getLogger('worker services')


async def write_items_service(data: List[Product]):
    try:
        for item in data:
            product = item.dict()
            db.insert_or_update_data('items', product,
                                     {"product_name": product["product_name"],
                                      "name_model": product["name_model"],
                                      "description": product["description"]})
    except Exception as e:
        logger.error(f"Unexpected error occurred {str(e)}")


async def write_streamers_service(streamers: Union[List[Streamer], Streamer]):
    try:
        for streamer in streamers:
            db.insert_or_update_data('streamers', streamer.dict(), {"id": streamer.id})
    except ValueError as e:
        logger.error(f"Streamer with this id already exists. {str(e)}")


    except Exception as e:
        logger.error(f"an unexpected error occurred {str(e)}")


async def write_games_service(data: List[Game]):
    try:
        for item in data:
            game = item.dict()
            db.insert_or_update_data('games', game, {"id": game["id"]})

    except ValueError:
        logger.error("Duplicate of unique key error")

    except Exception as e:
        logger.error(f"an unexpected error occurred {str(e)}")

    return JSONResponse(status_code=status.HTTP_200_OK, content='Parsed successfully')


async def write_streams(data: List[Stream]):
    for item in data:
        stream = item.to_dict()
        db.insert_or_update_data('streams', stream, {"id": stream['id']})


async def get_products_from_page(url) -> list:
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            cards = soup.find_all('div', class_='x-product-card__card')
            return get_products_info(cards)


def get_products_info(cards: List[bs4.element.Tag]):
    products = []

    for card in cards:
        try:
            price_tag = card.find_all('span')
            price = validate_price(price_tag)
            brand_name = card.find('div', class_='x-product-card-description__brand-name').text.strip()
            product_name = card.find('div', class_='x-product-card-description__product-name').text.strip()
            link = card.find('a', class_='x-product-card__link')['href']

            product = Product(
                price=price,
                product_name=product_name,
                name_model=brand_name,
                link=link
            )
            products.append(product)

        except ValidationError:
            logger.error('error while create Product object')

        except Exception as e:
            logger.error(f'Unexpected error {str(e)}')

    return products


async def get_category_products(url):
    logger.info('parser is started!')
    products = []
    page = 0

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()
            while True:
                curr_page = await generate_next_page_url(url, page)
                page_products = await get_products_from_page(curr_page)
                if len(page_products) != 0:
                    products.extend(page_products)
                    page += 1
                else:
                    break

    logger.info(products)
    logger.info(f"number of parsed products: {len(products)}")

    return products


async def get_brand_url(gender: str, brand_name: str) -> Union[str]:
    brand = None
    try:
        raw_data = db.find_one('brands', {"sex": gender, "name": brand_name.lower()})
        brand = Brand(**raw_data)

        return f'https://lamoda.by{brand.url}'

    except TypeError as e:
        print(str(e))
        logger.error(f'invalid data sent to server. {str(e)}')


async def write_categories(gender: str):
    try:
        data = await parse_categories(genders[gender])
        for item in data:
            query = {"name": item["name"], "sex": gender}
            db.update_data("categories", query, {**item, "sex": gender, "created_at": datetime.now()})
    except TypeError as te:
        logger.error(str(te))

    except Exception as e:
        logger.error(str(e))


def write_brands_names(brands: List):
    for el in brands:
        db.insert_one('brands', el)
