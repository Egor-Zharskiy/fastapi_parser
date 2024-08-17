import json
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
from fastapi import HTTPException, status

from lamoda.schemas import Product


def parse_categories(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    nav_panel = soup.find('nav', {"class": "d-header-topmenu"})
    categories = []
    for el in nav_panel.find_all('a'):
        cat_name = el.get_text(strip=True)
        categories.append({"name": cat_name, "url": el['href']}) if cat_name != '' else None
    return categories


async def get_products_from_page(url) -> list:
    links = []
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()

        soup = BeautifulSoup(text, 'html.parser')
        cards = soup.find_all('div', class_='x-product-card__card')

        for card in cards:
            link_tag = card.find('a', class_='x-product-card__link')
            if link_tag and 'href' in link_tag.attrs:
                links.append(link_tag['href'])

    return links


async def generate_next_page_url(base_url: str, current_page: int) -> str:
    if "?" in base_url:
        return f"{base_url}&page={current_page + 1}"
    else:
        return f"{base_url}?page={current_page + 1}"


async def get_category_products(url):
    product_links = []
    page = 0

    while True:
        curr_page = await generate_next_page_url(url, page)
        page_products = await get_products_from_page(curr_page)
        if len(page_products) != 0:
            product_links.extend(page_products)
            page += 1
        else:
            break

    tasks = [get_detailed_product(f"https://lamoda.by{link}") for link in product_links]
    all_products = await asyncio.gather(*tasks)
    return all_products


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

        price = None
        for el in price_tag:
            price_text = el.text.strip()
            if 'р.' in price_text:
                price = price_text

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed to parse information about the product")

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Unexpected error occurred")


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
