import random

def data_avilable():
    return random.randint(0, 10) % 2 == 0

def get_data():
    number = 1
    while True:
        if not data_avilable():
            yield
        else:
            yield range(number, number + 3)
            number += 3

def consume():
    while True:
        data = yield
        for datum in data:
            print('Data [{}] consumed'.format(datum))


def produce():
    while True:
        yield from get_data()

consumer = consume()
consumer.send(None)

producer = produce()

for iteration in range(10):
    data = next(producer)
    if data:
        consumer.send(data)
    else:
        print('No data, doing something else...')
