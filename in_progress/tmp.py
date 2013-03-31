def get_data():
    number = 1
    while True:
        yield range(number, number + 3)
        number += 3

def consume(data):
    iteration = yield
    print('Consume iteration #{}'.format(iteration))
    for datum in data:
        print('Data [{}] consumed'.format(datum))

def produce(source):
    while True:
        data = next(source)
        yield from consume(data)

producer = produce(get_data())
producer.send(None)
for iteration in range(10):
    producer.send(iteration)
