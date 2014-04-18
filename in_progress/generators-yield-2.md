## Cooperative Multi-tasking versus Preemptive Scheduling

Most operating systems, (and, thus, their threading APIs) are based upon
the idea of *preemption*. A single thread of execution may, at any time, be
*preemtped* by another thread of execution, if the *scheduler* decides it is
advantageous to do so. The *scheduler* is responsible for deciding which threads
should run at any given moment. Preemptive scheduling policies is a 
deep topic with many subtleties. Suffice it to say that most schedulers have
been based upon the notion of time-slicing (distributing small slices of
processing time evenly among competing processes). 

There is, however, another way to approach scheduling. Rather than 
processes *contending* for CPU time, what if they instead *collaborated*?
What might that collaboration look like? Ideally, a process would use the CPU until it
realized that it had to wait for data to be available (i.e. network I/O, disk
I/O, etc), at which point it would yield the CPU to another thread that *did*
have work to do. The word "yield" in the last sentence should jump out at you.

In the previous article we saw that the `yield` keyword gives Python a specialized
type of coroutine. What if, instead of being forced to yield control back to
the function that called it, a generator could yield to *another generator* (or
*subgenerator*)? This would be akin to the generator saying "I've done all the
work I can, and any additional work is dependent on the values yielded from the
following generator."

Using this concept we can implement what's called *cooperative multitasking* (or "cooperative
multi-threading"). Each potential thread of execution is trusted to yield
control whenever it would need to wait on something for a result or event. The scheduler,
therefore, is fairly straightforward: it may only change which thread is currently executing
once the previous one has yielded control (where it needs to wait anyway). The scheduler 
*may not* interrupt execution at any other point. 

So what does all of this have to do with the `yield` keyword? Well, if `yield` were
allowed to yield control to a subgenerator, you could write a simple scheduler
based on this concept and the result should be quite fast (compared to a
synchronous or preemptive alternative). The key, however, is that 
each "thread" (generator in our case) is trusted to `yield` when appropriate. 
A single bad-actor who never calls `yield` would effectively prevent 
any other code from being executed.

`yield from`, introduced in [PEP-380](http://www.python.org/dev/peps/pep-0380/), gives 
Python the power to, among other things, create a cooperative multitasking system. `yield from` is used
with an expression that evaluates to an `iterable`. This `iterable` `yield`s a
series of values and is run to exhaustion. The code that receives these values
is the code that called the generator with `yield from` (not the generator with
`yield from` itself).

Here's a stupid example of how it works:

    #!py
    def eleven_through_twenty():
        num = 11
        while num <= 20:
            yield num
            num += 1
        return num

    def one_to_thirty():
        num = 1
        while num <= 10:
            yield num
            num += 1

        num = yield from eleven_through_twenty()
        
        while num <= 30:
            yield num
            num += 1


    for value in one_to_thirty():
        print(value)

This will print the values from one to thirty. First, `one_to_thirty` `yield`s one
through ten. It next *delegates* value generation to a *sub-generator*:
`eleven_through_twenty`. That `generator` prints the next ten numbers and,
eventually, returns the number at which it stopped. `one_to_thirty` makes use of
this number (`num`) to further print the numbers `num` through thirty.

In the previous example, we saw how `yield from` can be used to delegate
generation to a sub-generator. We also saw that, like normal generators, a
sub-generator can return a value that the calling generator makes use of.

## Scheduling Generators

But we began this discussion about schedulers, so let's return to that topic.
The simplest possible scheduler would have a single queue of tasks
waiting to be executed. It would let each task execute to completion in turn. There
is no attempt at fairness; rather, the scheduler always lets each thread have as
much time as it wants. Really not much of a scheduler at all...

Such a scheduler would look roughly like the following:

    #!py

    run_queue = []

    def schedule(task):
        run_queue.append(task)

    def scheduler_loop():
        while run_queue:
            task = run_queue.pop(0)
            task.run()

That doesn't seem too useful (since each task would totally block any other task
from running). What if we knew the tasks would `yield` at some point? We could
create a coarse-grained *round robin* scheduler that ran each task until it
yielded. Once a task yields, it is moved to the end of the queue the next task
is popped off and run.

Enough theory, let's jump into some code. Our goal is to write a simple 
(generator) scheduler by making use of the fact that we know all functions will
yield at some reasonable point.

    #!py

    current = None
    ready = []
    
    def scheduler_loop():
        global current
        while ready:
            generator = ready[0]
        try:
            generator.next():
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

In this code sample we select a task, run it until it yields, then move it to
the end of the list and run the next task. Note that we don't yet have a way for
a task to indicate what it's waiting on (i.e. the reason it yielded), but that's
not important at the moment. With this scheduler, we could schedule a few simple
"tasks" like so:

    #!py
    def yield_n_times(value, iterations):
        for _ in range(iterations):
            yield value

    p1 = schedle(yield_n_times('hello', 3))
    p2 = schedule(yield_n_times(5, 2))
    p3 = schedule(yield_n_times(['sandwich', 'lawnmower'], 4))
    
    scheduler_loop()

This gives the following output:

    #!bash
    $ python3 generators.py
    hello
    5
    ['sandwich', 'lawnmower']
    hello
    5
    ['sandwich', 'lawnmower']
    hello
    ['sandwich', 'lawnmower']
    ['sandwich', 'lawnmower']

Note how each task was dispatched in the order it was scheduled. When a task
runs out of stuff to do, it is removed from the `ready` list. The `generator`
responsible for `yield`ing `['sandich', 'lawnmower']` performs two consecutive
runs at the end because no other valid unit of work exists.

## Moar Power (Part II)

While this is marginally interesting, a long-running task would not call `yield`
unless it had a good reason to do so. What might that reason be? Waiting on I/O,
for one. Any time a task makes a blocking call in a cooperative multitasking
environment, it results in *all* tasks being blocked by that call (since
said task can not call yield until *after* it has gotten the data it needs).

What exactly is a *blocking call*? Also known as the *synchronous* form of an
action, a blocking call is a function call which does not return until it has a
valid result. If the function is something like `recv()`, that means calls to
`recv()` will not return until there is actually data received.

In contrast, *non-blocking* (or *asynchronous*) functions are guaranteed to
return immediately. In the `recv()` example, it might simply return 0 straight
away if no data is available.

So the big question becomes: how can we make tasks yield when performing synchronous I/O
? More importantly, how would we know exactly *what* I/O a task is waiitng for? That
is, if I schedule a task that is willing to wait until the socket it opened is
readable, how do I store and check that information to know when to reschedule the
task?

## `select`, `poll`, and Event Loops

Luckily, the question of how a thread signals that it is waiting on I/O is a
solved problem. Using *file descriptor* sets, a thread registers the *file
descriptor* (an integer ID representing the file-like object in question)
associated with the socket or file stream from which it needs to read or write.

Two sets of file descriptors are usually used: a read set and a write set. An
*event loop* is created to loop continuously (i.e. `while True`) and check if
any of the file descriptors in each set are ready for reading/writing. The
actual check to determine if a file descriptor is ready to be used is done by
the system calls `select` and `poll`. 

Though their goal is the same, `select` and `poll` take different routes to
achieve it. `select` takes a `nfds` parameter which must be set to the highest
file descriptor number to check (file descriptor IDs begin at `0` and increase
by `1` for each new file descriptor). This works, however there's an implicit
inefficiency in checking using this method: all file descriptors from `0` to
`nfds` are checked, regardless of whether or not the programmer is actually
*interested* in all of those file descriptors. It's very common to be interested
in non-contiguous file descriptors that span a reasonably large range. If I'm
only interested in file descriptors `16` and `17`, `ndfs` would be set to `18`.
This causes the first `15` file descriptors to be checked needlessly.

`poll` improves on `select` by taking an array of `pollfd` objects. Each object
contains a file descriptor, a set of events that the programmer
corresponding entry in the read set is readable (or an entry in the write set is
writable). This implies that one needs to iterate over the bitset and check each
individual bit to determine if work can be done on that file descriptor. 

`poll`, on the other hand, does a similar check against a read set and a write
set, but returns a 
look at a simple example in psuedo-code:

    #!py
    while True:
        for ready_set in read_set
