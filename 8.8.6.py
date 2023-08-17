import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent

category_lst = []
pagen_lst = []
domain = "https://parsinger.ru/asyncio/create_soup/1/"
result = []
def get_soup(url):
    resp = requests.get(url=url)
    return BeautifulSoup(resp.text, 'lxml')

def get_urls_categories(soup):
    all_link = soup.find('div', class_='item_card').find_all('a')

    for cat in all_link:
        category_lst.append(domain + cat['href'])

async def get_data(session, link):
    retry_options = ExponentialRetry(attempts=5)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(link) as response:
        if response.ok:
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            result.append(int(soup.find('p', {'class':'text'}).text))


async def main():
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    async with aiohttp.ClientSession(headers=fake_ua) as session:
        tasks = []
        for link in category_lst:
            task = asyncio.create_task(get_data(session, link))
            tasks.append(task)
            await asyncio.gather(*tasks)

url = 'https://parsinger.ru/asyncio/create_soup/1/index.html'
soup = get_soup(url)
get_urls_categories(soup)

asyncio.run(main())

print(sum(result))
