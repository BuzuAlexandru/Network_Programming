import pika
import requests
from bs4 import BeautifulSoup
import re


class Crawler:
    def __init__(self, host, queue):
        self.host = host
        self.queue = queue

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True)

    def publish(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                   ))
        print(f" [x] Sent {message} to scrapper(s)")

    def crawl(self, url, url_list=None, max_page=1, count=1):
        if url_list is None:
            url_list = []

        response = requests.get(url + f'?page={count}')
        next_page = False
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if re.search('^/ro/\d{8}', str(href)) and 'https://999.md' + href not in url_list:
                    product_url = 'https://999.md' + href
                    url_list.append(product_url)
                    self.publish(product_url)

                elif re.search('page=+\d$', str(href)) and not next_page:
                    if int(re.sub('\D', '', href)) > count:
                        next_page = True

        if count < max_page and next_page:
            count += 1
            self.crawl(url, url_list, max_page, count)

        return url_list
