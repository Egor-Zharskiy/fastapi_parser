import re
from typing import Dict, List

from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
from fastapi import HTTPException

from database import db
from lamoda.schemas import Category


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


async def get_all_products_from(url):
    product_links = []
    page = 1

    while True:
        curr_page = url + f"&page={page}"
        page_products = await get_products_from_page(curr_page)
        if len(page_products) != 0:
            product_links.extend(page_products)
            page += 1
        else:
            break

    tasks = [get_detailed_product(f"https://lamoda.by{link}") for link in product_links]
    all_products = await asyncio.gather(*tasks)
    # print(all_products)
    return all_products


async def get_detailed_product(url) -> dict:
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()

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

    data = {
        'price': price,
        'product_name': product_name,
        'model_name': model_name,
        'rating': rating,
        'rating_count': rating_count,
        'description': description
    }
    return data


async def get_categories_service() -> list:
    raw_data = db.categories.find()
    categories = []
    for data in raw_data:
        try:
            category = Category(**data)
            categories.append(category)
        except Exception as e:
            print(e)

    return categories


async def get_cat_names() -> Dict[str, List[Category]]:
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
