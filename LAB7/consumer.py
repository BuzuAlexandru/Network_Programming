from utils.scrapper import Scrapper
import sys
import threading
from tinydb import TinyDB

# int(sys.argv[1]) or 1
num_workers = 10
host = 'localhost'
queue = 'lab7'
lock = threading.Lock()


def handle_consumer(index):
    Scrapper(f'S{index}', host, queue, lock)


if __name__ == '__main__':
    try:
        print('To exit press CTRL+C')
        for i in range(num_workers):
            consumer_thread = threading.Thread(target=handle_consumer, args=(i + 1,))
            consumer_thread.start()

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            exit()
