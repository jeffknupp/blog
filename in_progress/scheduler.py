runnable = []
current = None

def scheduler_loop():
    while runnable:
        generator = runnable[0]
        try:
            value = generator.next()
        except StopIteration:
            runnable.remove(generator)
        else:
            round_robin(generator)

def round_robin(generator):
    if runnable and runnable[0] is generator:
        del runnable[0]
        runnable.append(generator)

def block(queue):
    queue.append(current)
    runnable.remove(current)

def unblock(queue):
    if queue:
        generator = queue.pop(0)
        runnable.append(generator)

def person(name, count):
    for i in xrange(count):
        print name, 'running'
        yield

def producer(n):
    for i in xrange(n):
        yield 'item'

def consumer(item):
    print item
    yield

runnable.appen(producer(5))
runnable.append(consumer())

