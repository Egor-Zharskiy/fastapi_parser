import json
from typing import List

import bs4
from bs4 import BeautifulSoup
import requests
import aiohttp
from pydantic import ValidationError

from workers.schemas.schemas import Product
from workers.utils.utils import validate_price

import logging

logger = logging.getLogger("Lamoda Services")


async def parse_categories(url: str) -> list:
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            nav_panel = soup.find('nav', {"class": "d-header-topmenu"})
            categories = []
            for el in nav_panel.find_all('a'):
                cat_name = el.get_text(strip=True)
                categories.append({"name": cat_name, "url": el['href']}) if cat_name != '' else None
    return categories


async def get_products_from_page(url) -> list:
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()

        soup = BeautifulSoup(text, 'html.parser')
        cards = soup.find_all('div', class_='x-product-card__card')

    return await get_products_info(cards)


async def get_products_info(cards: List[bs4.element.Tag]) -> List[Product]:
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
            logger.info('error while create Product object')

        except Exception as e:
            logger.info(f"Unexpected error {str(e)}")

    return products


async def generate_next_page_url(base_url: str, current_page: int) -> str:
    if "?" in base_url:
        return f"{base_url}&page={current_page + 1}"
    else:
        return f"{base_url}?page={current_page + 1}"


async def get_category_products(url):
    products = []
    page = 0

    while True:
        curr_page = generate_next_page_url(url, page)
        page_products = await get_products_from_page(curr_page)
        if len(page_products) != 0:
            products.extend(page_products)
            page += 1
        else:
            break

    logger.info(products)
    logger.info(f"Number of parsed products: {len(products)}")

    return products


async def get_detailed_product(url) -> Product:
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()

    try:
        soup = BeautifulSoup(text, 'html.parser')
        product_name = soup.find('span', class_="x-premium-product-title__brand-name").text.strip()
        model_name = soup.find('div', class_="x-premium-product-title__model-name").text.strip()
        price_tag = soup.find_all('span', class_="x-premium-product-prices__price")
        rating_count_tag = soup.find('div', class_="product-rating__count")
        rating_tag = soup.find('div', class_="product-rating__stars-inner")

        try:
            rating = float(rating_tag.get('style').split('width:')[1].split('%')[0]) * 5 / 100
            rating_count = rating_count_tag.text.strip()
        except AttributeError:
            rating = None
            rating_count = None

        price = validate_price(price_tag)

        description_tags = soup.find_all(class_="x-premium-product-description-attribute")
        description = {}
        for el in description_tags:
            attr = el.text.strip().split('.')
            description[attr[0]] = attr[-1]

        data = Product(
            price=price,
            product_name=product_name,
            name_model=model_name,
            rating=rating,
            rating_count=rating_count,
            description=description
        )

        return data

    except AttributeError:
        logger.error("Failed to parse information about the product")

    except Exception as e:
        logger.error(f"Unexpected error occurred {str(e)}")


def parse_brands(url: str) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    text = response.text.split('payload:')[2].split(""",\n        settings:""")[0]
    data = json.loads(text)
    brands = []
    for line in data['data']:
        for brand in line['brands']:
            brands.append({'name': brand['name'].lower(), 'url': brand['url'], "sex": "kids"})

    return brands
