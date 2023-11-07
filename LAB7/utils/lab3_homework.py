import requests
from bs4 import BeautifulSoup
import sys


def scrapper(url):
    try:
        response = requests.get(url)
    except ConnectionError:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    info = dict()

    info['URL'] = url

    try:
        info["Product"] = soup.find('h1').get_text()
    except:
        pass

    try:
        info["Seller"] = soup.find('a', {'class': 'adPage__aside__stats__owner__login buyer_experiment'}).get_text()
    except:
        pass

    try:
        info["Last update"] = (soup.find('div', {'class': 'adPage__aside__stats__date'})
                               .get_text().replace('Data actualizării: ', ''))
    except:
        pass

    try:
        info["Transaction"] = (soup.find('div', {'class': 'adPage__aside__stats__type'})
                               .get_text().replace('Tipul: ', ''))
    except:
        pass

    try:
        info["Price"] = soup.find('span', {'class': 'adPage__content__price-feature__prices__price__value'}).get_text()

    except:
        pass

    try:
        currency = soup.find('span', {'class': 'adPage__content__price-feature__prices__price__currency'})
        if currency:
            info["Price"] += currency.get_text()
    except:
        pass

    characteristics = []
    info['Extra'] = []
    for div in soup.findAll('div', {'class': 'adPage__content__features'}):

        for characteristics_div in div.findAll('div', {'class': 'adPage__content__features__col grid_9 suffix_1'}):
            for ul in characteristics_div.findAll('ul'):
                for attribute in ul.findAll('span'):
                    characteristics.append(attribute.text.lstrip().rstrip())

            for i in range(0, len(characteristics) - 1, 2):
                info.update({characteristics[i]: characteristics[i + 1]})

        for options_div in div.findAll('div', {'class': 'adPage__content__features__col grid_7 suffix_1'}):
            for ul in options_div.findAll('ul'):
                for attribute in ul.findAll('span'):
                    info["Extra"].append(attribute.text.lstrip().rstrip())

    description = 'No description'

    if (desc1 := soup.find('div', {'class': 'adPage__content__description grid_17'})) is not None:
        description = desc1.get_text()
    elif (desc1 := soup.find('div', {'class': 'adPage__content__description grid_18'})) is not None:
        description = desc1.get_text()
    elif (desc1 := soup.find('div', {'class': 'adPage__content__description grid_19'})) is not None:
        description = desc1.get_text()

    info.update({"Description": description})

    return info

# product = 'https://999.md/ro/80845265'
# for k, v in scrapper(product).items():
#     print(f'{k} : {v}')
