import requests
from bs4 import BeautifulSoup
import re


def crawl(url, url_list=[], max_page=1, count=1):
    response = requests.get(url+f'?page={count}')
    next_page = False
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if re.search('^/ro/\d{8}', str(href)) and 'https://999.md'+href not in url_list:
                url_list.append('https://999.md'+href)

            elif re.search('page=+\d$', str(href)) and not next_page:
                if int(re.sub('\D', '', href)) > count:
                    next_page = True

    if count <= max_page and next_page:
        count += 1
        crawl(url, url_list, max_page, count)

    return url_list


page = 'https://999.md/ro/list/transport/oil-additives'

with open('./result.txt', 'w') as f:
    for url in crawl(page, max_page=6):
        f.write(url+'\n')
