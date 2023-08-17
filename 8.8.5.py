import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_socks import ChainProxyConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent

category_lst = []
pagen_lst = []
domain = 'https://parsinger.ru/html/'
result = []
def get_soup(url):
    resp = requests.get(url=url)
    return BeautifulSoup(resp.text, 'lxml')

def get_urls_categories(soup):
    all_link = soup.find('div', class_='nav_menu').find_all('a')

    for cat in all_link:
        category_lst.append(domain + cat['href'])

def get_urls_pages(category_lst):
    for cat in category_lst:
        resp = requests.get(url=cat)
        soup = BeautifulSoup(resp.text, 'lxml')
        for pagen in soup.find('div', class_='pagen').find_all('a'):
            pagen_lst.append(domain + pagen['href'])

async def get_data(session, link):
    retry_options = ExponentialRetry(attempts=5)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(link) as response:
        if response.ok:
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            item_card = [x['href'] for x in soup.find_all('a', class_='name_item')]
            for x in item_card:
                url2 = domain + x
                async with session.get(url=url2) as response2:
                    resp2 = await response2.text()
                    soup2 = BeautifulSoup(resp2, 'lxml')
                    price = int(soup2.find('span', id='price').text.split()[0])
                    old_price = int(soup2.find('span', id='old_price').text.split()[0])
                    count = int(soup2.find('span', id='in_stock').text.split()[2])
                    result.append((old_price-price)*count)

async def main():
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    '''connector = ChainProxyConnector.from_urls(
        [
            'socks5://144.217.197.151:39399',
            'socks5://167.71.241.136:33299',
        ]
    )'''
    async with aiohttp.ClientSession(headers=fake_ua) as session:
        tasks = []
        for link in pagen_lst:
            task = asyncio.create_task(get_data(session, link))
            tasks.append(task)
            await asyncio.gather(*tasks)

url = 'https://parsinger.ru/html/index1_page_1.html'
soup = get_soup(url)
get_urls_categories(soup)
get_urls_pages(category_lst)
asyncio.run(main())
print(len(result))
