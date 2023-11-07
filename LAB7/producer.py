from utils.crawler import Crawler


host = 'localhost'
queue = 'lab7'

crawler = Crawler(host, queue)

url = 'https://999.md/ro/list/transport/oil-additives'
_ = crawler.crawl(url, max_page=1)
