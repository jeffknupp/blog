
current = None
ready = []

def scheduler_loop():
    global current
    while ready:
        generator = ready[0]
        try:
            print(next(generator))
        except StopIteration:
            unschedule(generator)
        else:
            round_robin(generator)

def round_robin(generator):
    if ready and ready[0] is generator:
        del ready[0]
        ready.append(generator)

def schedule(g):
    ready.append(g)

def unschedule(g):
    if g in ready:
        ready.remove(g)


def yield_n_times(value, iterations):
    for _ in range(iterations):
        yield value

p1 = schedule(yield_n_times('hello', 3))
p2 = schedule(yield_n_times(5, 2))
p3 = schedule(yield_n_times(['sandwich', 'lawnmower'], 4))

scheduler_loop()
