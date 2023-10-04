import socket
import json
from bs4 import BeautifulSoup


def tcp_parser():
    HOST = '127.0.0.1'
    PORT = 8080

    def send_request(link):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(f'GET {link} HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n'.encode())
        response = sock.recv(1024)
        sock.close()
        return BeautifulSoup(response.decode(), 'html.parser')

    home = '/'
    about = '/about'
    contacts = '/contacts'
    products = '/products'

    content = dict()
    content['home'] = send_request(home).find('h1').get_text()
    content['about'] = send_request(about).find('p').get_text()
    content['contacts'] = send_request(contacts).find('p').get_text()
    product_list = send_request(products)
    content['products'] = product_list.find('h1').get_text()
    content['product_list'] = []

    for product in product_list.findAll('a'):
        content['products'] += '\n' + product.get_text()
        href = product.get('href')
        prod_info = send_request('/'+href)
        info = prod_info.findAll('p')
        prod = {
            'name': prod_info.find('h1').get_text(),
            'author': info[0].get_text(),
            'price': float(info[1].get_text()),
            'description': info[2].get_text()
        }

        content['product_list'].append(prod)

    return content


result = json.dumps(tcp_parser(), indent=4)
print(result)
with open('./scraped_content.json', 'w') as f:
    f.write(result)
