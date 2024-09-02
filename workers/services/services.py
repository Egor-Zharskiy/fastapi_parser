from typing import List, Union

import bs4.element
import requests
from bs4 import BeautifulSoup

from fastapi.responses import JSONResponse
from pydantic import ValidationError

from workers.database import MongoConnection
from workers.schemas.schemas import Product, Brand
from workers.schemas.schemas import Streamer, Game, Stream
from fastapi import status, HTTPException

from workers.services.parsers.lamoda_parser import generate_next_page_url
from workers.utils.utils import validate_price

db = MongoConnection()


def write_items_service(data: List[Product]):
    try:
        for item in data:
            product = item.dict()
            db.insert_or_update_data('items', product,
                                     {"product_name": product["product_name"],
                                      "name_model": product["name_model"],
                                      "description": product["description"]})
    except Exception as e:
        print(f"Unexpected error occurred {str(e)}")


def write_streamers_service(streamers: Union[List[Streamer], Streamer]):
    try:
        for streamer in streamers:
            db.insert_or_update_data('streamers', streamer.dict(), {"id": streamer.id})
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Streamer with this id already exists.")

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="an unexpected error occurred")


def write_games_service(data: List[Game]):
    try:
        for item in data:
            game = item.dict()
            db.insert_or_update_data('games', game, {"id": game["id"]})

    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Duplicate of unique key error")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="an unexpected error occurred")

    return JSONResponse(status_code=status.HTTP_200_OK, content='Parsed successfully')


def write_streams(data: List[Stream]):
    for item in data:
        stream = item.to_dict()
        db.insert_or_update_data('streams', stream, {"id": stream['id']})


def get_products_from_page(url) -> list:
    response = requests.get(url)
    text = response.text

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
            print('error while create Product object')

        except Exception as e:
            print(f"Unexpected error {str(e)}")

    return products


def get_category_products(url):
    print('parser is started!')
    products = []
    page = 0

    while True:
        curr_page = generate_next_page_url(url, page)
        page_products = get_products_from_page(curr_page)
        if len(page_products) != 0:
            products.extend(page_products)
            page += 1
        else:
            break

    print(products)
    print(f"number of parsed products: {len(products)}")

    return products


def get_brand_url(gender: str, brand_name: str) -> Union[str, Exception]:
    try:
        raw_data = db.find_one('brands', {"sex": gender, "name": brand_name.lower()})
        brand = Brand(**raw_data)

    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid data sent to server.')

    return f'https://lamoda.by{brand.url}'
