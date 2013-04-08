## `yield`: More Than Simple Iteration

When `generators` were first introduced in Python, they had some restrictions: 

* A `generator` could only yield a value to the code that invoked it
* A `generator` which `yield`ed the value of *another* generator yielded a
    `generator object` rather than the *value* `yield`ed by the generator it
     called. For example, in the code below the value printed in the `for` 
     loop would be `<generator object foo at 0xdeadbeef00000000>` because
    `bar` was essentially `yield`ing a `generator object` "wrapping" the 
    `generator object` created by `foo`.  

    #!py
    def foo(value):
        value = yield (value + 2)

    def bar():
        current = 0
        while True:
            yield foo(current)
            current += 1

    b = bar()
    next(b)
    for value in range(10):
        print(next(b))

* After a `generator object` was created, the communication was one-way only; it sent you values. 
  You couldn't send *it* anything.


## Moar Power

In [PEP 342](http://www.python.org/dev/peps/pep-0342/), support was added for passing values *into* generators. 
[PEP 342](http://www.python.org/dev/peps/pep-0342/) gave `generator`s the power to yield a value (as before), *receive* a
value, or both yield a value *and* receive a (possibly different) value in a 
single statement. 

*By doing so, [PEP 342](http://www.python.org/dev/peps/pep-0342/) effectively allowed a generator to call other functions or generators without blocking. This gave `yield` the power to create proper `coroutines`.  More on this later.*

To illustrate how values are sent to a `generator`, let's return to our 
prime number example. This time, instead of simply printing 
every prime number greater than `number`, we'll find the smallest prime 
number greater than successive powers of a number (i.e. for 10, we get 
the smallest prime greater than 10, then 100, then 1000, etc.). 
We start in the same way as `get_primes`:

    #!py
    def print_successive_primes(base=10, iterations):
        # like normal functions, a generator function
        # can be assigned to a variable

        prime_generator = get_primes(base)
        # missing code...
        for power in range(iterations):
            # missing code...

    def get_primes(number):
        while True:
            if is_prime(number):
            # ...

The next line of `get_primes` takes a bit of explanation. While `yield number` would yield the
value of `number`, a statement of the form `other = yield foo` means, "yield `foo` and,
when a value is sent to me, set `other` to that value." You can "send" values to
a generator using the generator's `send` method.

    #!py
    def get_primes(number):
        while True:
            if is_prime(number):
                number = yield number
            number += 1

In this way, we can set `number` to a different value each time the generator
`yield`s. We can now fill in the missing code in `print_successive_primes`:

    #!py
    def print_successive_primes(base=10, iterations):
        prime_generator = get_primes(base)
        prime_generator.send(None)
        for power in range(iterations):
            print(generator.send(base ** power))

Two things to note here: First, we're printing the result of `generator.send`,
which is possible because `send` both sends a value to the generator *and*
returns the value yielded by the generator (mirroring how `yield` works from
within the `generator function`). 

Second, notice the `generator.send(None)` line. When you're using send to "start" a generator 
(that is, execute the code from the first line of the generator function up to
the first `yield` statement), you must send `None`. This makes sense, since by definition
the generator hasn't gotten to the first `yield` statement yet, so if we sent a
real value there would be nothing to "receive" it. Once the generator is started, we
can send values as we do above.

### Finally: `yield`'s Full Power

After [PEP 342](http://www.python.org/dev/peps/pep-0342/) enhanced the power 
of `yield`, [PEP 380](http://www.python.org/dev/peps/pep-0380/) gave `generator`s the final piece of the puzzle: control over where they `yield`ed to. Instead of
`yield` always returning a value to the calling function, a `generator function`
could "delegate" its `yield` to another `generator` (called a `subgenerator`).

In practical terms, just like before we could `yield` the value
returned by a function call (e.g. `yield is_prime(10)`), we can now yield the
*value* returned by a subgenerator without worrying about if we're getting back
a proper value or a `generator object`.

This effectively means that multiple `generators` can create a sort of 
symbiotic relationship, yielding back and forth between one another. 
When might this be useful? 

<a id="coro"></a>
## Coroutines, Asynchronous I/O, and Cooperative Multitasking

Let's implement a simple producer/consumer system. 
In a typical implementation, we would use a queue available to 
both `produce` and `consume`, each of which runs on a separate thread. 
Here's an example (equivalent to our `produce` and `consume` description) 
[from the Python documentation](http://:

    #!py
    def worker():
        while True:
            item = q.get()
            do_work(item)
            q.task_done()

    q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for item in source():
        q.put(item)

    q.join()    

Becuase it is shared between multiple threads, access to the `Queue` must be synchronized.
In this case, it's straightforward because Python's
`Queue` class manages access internally. In the real world,
use of shared data between threads common. It is also a recipe for race 
conditions, deadlocks, thread starvation, and all the other attendant issues 
of multi-threaded code.

There's another way to implement a producer/consumer in Python, however.
Dave Beazly has [an excellent set of slides and examples](http://www.dabeaz.com/coroutines/) on using coroutines
to do (among other things) `cooperative multitasking`.  If we 
implement `produce` and `consume` as coroutines, we avoid
the pains of multithreading. `produce` yields data to `consume` each time it is
called. `consume` simply yields until data is available, processes it, then
resumes waiting for data by yielding. 

The scheduler takes care of managing the interaction between `produce` 
and `consume`, but in a very generic way. It knows how to 
dispatch `coroutines` and queue up `coroutines` to be run. It knows
nothing about what the tasks are actually doing (producing and consuming in this
case). **This is a powerful idea.** If we could write one "perfect" scheduler,
we could perform cooperative multitasking without needing to change our
programming paradigms.

Two interesting things to note here. Only one coroutine is executing at any
time, so data sharing issues disappear. Also, the execution pattern 
of `consume` is the basis for a large number of asynchronous IO frameworks.
Like `consume`, work is done until some resource is required, at which point
the coroutine yields.

### Tulip: The Future of Asynchronous I/O in Python

Lack of first-party support for asynchronous I/O has hurt Python a bit, especially when 
node.js showed how powerful it can be. It has been discussed quite frequently on
the python-dev dlist. Towards the end of last year, however, discussions about how asynchronous I/O 
should be implemented in Python were all over python-dev. GvR created a number
of discussion threads exploring different approaches. Ultimately, he began a reference
implementation called . It's an
async I/O library that provides an event loop-and-callback style interface. This
is useful for interoperability with existing third-party async I/O frameworks
like Twisted and Tornado. But the BDFL (and many others)
aren't in love with frameworks that rely on callbacks. 

As an alternative, there's a scheduler for `coroutine` based 
asynchronous I/O and additional support from the library 
(in the form of `Tasks`) for using `coroutines` with the event loop. The Tulip
library is a perfect example of how powerful the combination of  
PEP 342's `send` and PEP 380's `yield from` can be. 

Hopefully, this post has made it clear that `yield` can do far more than simple
iteration. Understanding `yield` at a fundamental level allows you to express
algorithms (especially those involving state machines) in an elegant and
easy-to-read way. And, after all, elegance and clarity are what we're after,
right?

[^1]: A refresher: a prime number is a positive integer greater than 1
    that has no divisors other than 1 and itself. 3 is prime because there are no
    numbers that evenly divide it other than 1 and 3 itself.*

