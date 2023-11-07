import pika
from tinydb import TinyDB, Query
from .lab3_homework import scrapper


class Scrapper:
    def __init__(self, name, host, queue, lock):
        self.name = name
        self.host = host
        self.queue = queue
        self.lock = lock

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True)

        def callback(ch, method, properties, body):
            url: str = body.decode()
            print(f" [{self.name}] Received {url}")

            db = TinyDB('db.json')
            Product = Query()
            data = scrapper(url)

            if data is None:
                print(f" [{self.name}] Could not scrap")
                ch.basic_reject(delivery_tag=method.delivery_tag)
            else:
                with lock:
                    entry = db.get(Product['URL'] == url)
                    if entry is None:
                        db.insert(data)
                    else:
                        db.update(data, doc_ids=[entry.doc_id])

                print(f" [{self.name}] Done")
                ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(queue=self.queue, on_message_callback=callback)

        print(f' [{self.name}] Waiting for messages')
        self.channel.start_consuming()
