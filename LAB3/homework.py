import requests
from bs4 import BeautifulSoup
import sys


def scrapper(url):
    # try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        info = dict()

        try:
            info["Product"] = soup.find('h1').get_text()
        except:
            pass

        try:
            info["Seller"] = soup.find('a', {'class': 'adPage__aside__stats__owner__login buyer_experiment'}).get_text()
        except:
            pass

        info["Last update"] = (soup.find('div', {'class': 'adPage__aside__stats__date'})
                               .get_text().replace('Data actualizării: ', ''))

        info["Transaction"] = (soup.find('div', {'class': 'adPage__aside__stats__type'})
                               .get_text().replace('Tipul: ', ''))

        info["Price"] = soup.find('span', {'class': 'adPage__content__price-feature__prices__price__value'}).get_text()
        currency = soup.find('span', {'class': 'adPage__content__price-feature__prices__price__currency'})
        if currency:
            info["Price"] += currency.get_text()

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

        info.update({"Description": soup.find('div', {'class': 'adPage__content__description grid_18'}).get_text()})

    # except:
    #     print('Invalid link')
    #     sys.exit()

        return info


product = 'https://999.md/ro/82333904'
# product = 'https://999.md/ro/84339368'
for k, v in scrapper(product).items():
    print(f'{k} : {v}')
