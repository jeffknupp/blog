import random

def data_avilable():
    """Return True or False randomly"""
    return random.randint(0, 1) % 2 == 0

def get_data():
    """Represents a non-blocking function which gets data"""
    data_queue = []
    number = 0
    while True:
        if not data_avilable():
            data_queue += range(number, number + 3)
            number += 3
        else:
            yield data_queue
            data_queue = []

def consume(data_queue):
    while True:
        data_queue += (yield) or []
        while data_queue:
            print('Current data queue: {}'.format(data_queue))
            for _ in range(3):
                datum = data_queue.pop(0)
                print('Data [{}] consumed'.format(datum))
            data_queue += (yield) or []


def produce(consumer):
    while True:
        yield from get_data()

consumer = consume([])
consumer.send(None)

producer = produce(consumer)

for i in range(10):
    print('Asking for data')
    data = next(producer)
    if data:
        print('Got data {}'.format(data))
        consumer.send(data)
    else:
        print('Consuming data if possible...')
        next(consumer)
