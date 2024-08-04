import re

from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp


def parse_categories(url) -> list:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    nav_panel = soup.find('nav', {"class": "d-header-topmenu"})
    categories = []
    for el in nav_panel.find_all('a'):
        cat_name = el.get_text(strip=True)
        categories.append({"name": cat_name, "url": el['href']}) if cat_name != '' else None
    return categories


def get_products_from_page(url) -> list:
    response = requests.get(url)
    response.raise_for_status()
    links = []

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', class_='x-product-card__card')

    for card in cards:
        link_tag = card.find('a', class_='x-product-card__link')
        if link_tag and 'href' in link_tag.attrs:
            links.append(link_tag['href'])
    print(links)
    print(len(links))
    return links


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
    all_products = []
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
    # for link in product_links:
    #     product_url = f"https://lamoda.by{link}"
    #     product_data = get_detailed_product(product_url)
    #     all_products.extend(product_data)
    tasks = [get_detailed_product(f"https://lamoda.by{link}") for link in product_links]
    all_products = await asyncio.gather(*tasks)
    print(all_products)
    return all_products


async def get_detailed_product(url) -> dict:
    async with aiohttp.ClientSession() as session:
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

# get_detailed_product("https://www.lamoda.by/p/rtlaco494801/beauty_accs-perioe-zubnaya-pasta/")
# get_all_products_from('https://www.lamoda.by/c/4288/beauty_accs-menbeauty/?sitelink=topmenuM&l=8')
# get_products_from_page("https://www.lamoda.by/c/4288/beauty_accs-menbeauty/?sitelink=topmenuM&l=8")
