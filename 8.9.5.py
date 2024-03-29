import aiofiles
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import os

domain = 'https://parsinger.ru/asyncio/aiofile/2/'
category_lst = []

def get_folder_size(filepath, size=0):
    for root, dirs, files in os.walk(filepath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size

def get_soup(url):
    resp = requests.get(url=url)
    return BeautifulSoup(resp.text, 'lxml')

def get_urls_pages(soup):
    all_link = soup.find('div', class_='item_card').find_all('a')

    for cat in all_link:
        category_lst.append(domain + cat['href'])

async def write_file(session, url, name_img):
    async with aiofiles.open(f'images/{name_img}', mode='wb') as f:
        async with session.get(url) as response:
            async for x in response.content.iter_chunked(1024):
                await f.write(x)
        print(f'Изображение сохранено {name_img}')

img_url = []
async def main():
    async with aiohttp.ClientSession() as session:
        for url in category_lst:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                img_url.extend([x["src"] for x in soup.find_all('img')])

        tasks = []
        for link in set(img_url):
            name_img = link.split('/')[6]
            task = asyncio.create_task(write_file(session, link, name_img))
            tasks.append(task)
        await asyncio.gather(*tasks)

url = 'https://parsinger.ru/asyncio/aiofile/2/index.html'
soup = get_soup(url)
get_urls_pages(soup)
asyncio.run(main())

print(get_folder_size('selenium_env/images/'))