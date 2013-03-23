*Note: This post discusses generators and the `yield` keyword without assuming
any prior knowledge. If you're already familiar with the ins and outs of
`yield`, you can skip down to the section: 
[Coroutines, Asynchronous I/O, and Cooperative Multitasking](#coro)

##Understanding `yield` and Generators

When we call a normal Python function, execution starts at function's first line
and continues until a `return` statement, `exception`, or the end of the
function is encountered (which returns `None`).
Once a function returns control to it's caller, that's it. All of the variables
used in the function are destroyed, and a new call to the function starts
everything from the beginning.

This is all very standard when discussing functions (or *subroutines*) in most
programming languages. There are times, though, when it's beneficial to have
the ability to create a function which, instead of simply returning a single
value, is able to yield a series of values. To do so, it would have to 
"remember" where it left off each time.

Earlier, I said "yield a series of values" because out hypothetical function 
doesn't "return" in the normal sense. `return` implies that the function is "returning" execution 
to the point at which it was called. "Yield," however, implies that the transfer of control is
temporary and voluntary, and our function expects to regain it in the future.

"Functions" with these capabilites are called `generators`, and they're incredibly useful. 
The `yield` statement was initially introduced to give programmers the ability to 
create a `generator function` in much the same way they already wrote normal
functions. Consider the following example where the main issue is controlling 
iteration:

### Example: Fun With Prime Numbers

Suppose our boss asks us to write a function that takes a `list` of `int`s and 
returns all the elements which are prime numbers [^prime]. The only
additional requirement is that he needs to be able to iterate over the results.

"Simple," we say, and we write the following:

    #!py
    def get_primes(input_list):
        result_list = list()
        for element in input_list:
            if is_prime(element):
                result_list.append()
    
    # or better yet...

    def get_primes(input_list):
        return [element for element in input_list if is_prime(element)]

    # not germane to the example, but here's a possible implementation of
    # is_prime...
    
    def is_prime(number):
        if number > 1:
            if number == 2:
                return True
            if number % 2 == 0:
                return False
            for current in range(3, int(math.sqrt(number) + 1), 2):
                if number % current == 0: 
                    return False
            return True
        return False

Either `is_prime` implementation above fulfills the requirements, so we tell our 
boss we're done.

#### Dealing With Infinite Sequences

Later, our boss comes back tells us our function is working
great, but there's a problem: he wants to use our `get_primes` function on a
very large list of numbers. In fact, the list is so large that merely creating 
it would use all the memory on the system. To work around this, he wants to be 
able to call `get_primes` with a `start` value and get all the primes 
larger than `start` (perhaps he's solving [Project Euler problem 10](http://projecteuler.net/problem=10)).

This is obviously not a simple change to `get_primes`. Clearly, we can't return a 
list of all the prime numbers from `start` to infinity. Operating on infinite
sequences, though, has a wide range of useful applications. Our issue stems from
how normal functions are executed. In `get_primes`,
it would be nice if instead of returning all of the values, we could 
just return the *next* value. Then we're not creating a list at all. No list,
no memory issues. And because our boss told us he's just iterating 
over the results, he wouldn't know the difference. 

But that doesn't seem possible using a normal function. Even if we had a 
magical function that we could iterate from `n` to `infinity`, we'd get 
stuck after returning the first value:

    #!py
    def get_primes(start):
        for element in magical_infinite_range(start):
            if is_prime(element):
                return element

Imagine `get_primes` is called like so:

    #!py

        def solve_number_10():
            # He *is* working on Project Euler #10, I knew it!
            total = 2
            for next_prime in get_primes(3):
                if next_prime < 2000000:
                    total += next_prime
                else:
                    print(total)
                    return

In `get_primes`, we would hit the number `3` and return at line 4.
But what about generating the next value? Instead of `return`, we need a way to
return an "intermediate" value and, when asked for next value, pick up where 
we left off.

Functions, though, can't do this. When they `return`, they're
done for good. Even if we could guarantee a function would be called again, we
have no way of saying, "OK, now, instead of starting at the first line like
we normally do, start up where we left off at line 4." Functions have a single `entry
point`: the first line.

## Enter Generators

A `generator function` looks like a normal function, but whenever it needs to generate a
value, it uses `yield` instead of `return`. Those names are quite
descriptive. As I said in the introduction, `yield` implies "I am voluntarily giving 
up execution control for a while." `return` says, "return to wherever you were before 
you called me."

In Python, any time the code following a `def` contains the `yield` keyword, the result is 
not a normal function but a `generator function`. `generator functions`
automatically define a few methods, one of which is `__next__`. Since any object 
defining a `__next__` method can be iterated over, `generator functions` can be
used in a `for` loop like any other `Iterable`.

When we write our `get_primes` function as a `generator`, we no longer need 
the `magical_infinite_range` function. Since `generators` "remember" both where
they left off *and* the values of their variables, we can create our own infinite
sequence:

    #!py
    def get_primes(start):
        while True:
            if is_prime(start):
                yield start
            start += 1


It's helpful to visualize how the first few elements are created when we call
`get_primes` in `solve_number_10`'s `for` loop. When the `for` loop requests the first `next_prime`, 
we enter `get_primes` as we would in a normal function: from the first line. 
We enter the `while` loop, the `if` condition holds (`3` is prime) so we yield 
the value `3` and control to ` solve_number_10`.  The `for` loop then requests 
the next element from `get_primes`. Instead of starting back at the top, we 
resume at line 4, where we left off.


    #!py
    def get_primes(start):
        while True:
            if is_prime(start):
                yield start
            start += 1 <<<<<<<<<

Most importantly, `start` *still has the same value it did when we called* `yield`
(i.e. `3`). Clearly, then, `start` is incremented to `4`, we hit the top of the `while` loop, and 
keep incrementing start until we hit the next prime (`5`). Again we `yield` the 
value of `start` to the `for` loop. This continues until the `for` loop
stops (at the first prime greater than `2,000,000`).

Note that, just like with iterators, we are free to assign a `generator
function` to a variable and call `next()` on it directly. The following would
print the first three primes greater than or equal to `3`:

    #!py
    generator = get_primes(3)
    print(next(generator))
    print(next(generator))
    print(next(generator))

## `yield`: More Than Simple Iteration

When `generators` were first introduced in Python, they had some restrictions: 

* A `generator` could only yield a value to the code that invoked it
* A `generator` which `yield`ed the value of *another* generator yielded a
    `generator object` rather than the actual value `yield`ed by the generator it
     called. For example, in the code below the value printed in the `for` 
     loop would be `<generator object foo at 0xdeadbeef00000000>` because
    `bar` was `yield`ing the value of another generator: `foo`.  

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

* After a `generator` was created, the communication was one-way only; it sent you values. 
  You couldn't send *it* anything.

## Moar Power

In PEP 342, support was added for passing values *into* generators. 
PEP 342 gave `generator`s the power to yield a value (as before), *receive* a
value, or both yield a value and receive a (possibly different) value in a 
single statement.

*By doing so, it effectively allowed a generator to call other functions
or generators without blocking. More on this later.*

To illustrate how values are sent to a `generator`, let's return to our 
prime number example. This time, instead of simply printing 
every prime number greater than `start`, we'll find the smallest prime 
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

    def get_primes(start):
        while True:
            if is_prime(start):
            # ...

The next line of `get_primes` takes a bit of explanation. While `yield start` would yield the
value of `start`, a statement of the form `other = yield foo` means, "yield `foo` and,
when a value is sent to me, set `other` to that value." You can "send" values to
a generator using the generator's `send` method.

    #!py
    def get_primes(start):
        while True:
            if is_prime(start):
                start = yield start
            start += 1

In this way, we can set `start` to a different value each time the generator
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

After a series of PEPs enhancing the power of `yield`, PEP 380 gave `generator`s
the final piece of the puzzle: control over to whom you `yield`. 

This means that multiple `generators` can create a sort of symbiotic relationship,
yielding back and forth between one another. When might this be useful? Let's
implement a simple producer/consumer system. In a typical implementation, 
we would use a queue available to both `produce` and `consume`, each of which runs
on a separate thread. Here's an example from the Python documentation:

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

Here, access to the `Queue` must be synchronized. It is data shared
between multiple threads. In this case, it's straightforward because
`Queue` class manages access internally. In a more realistic situation
use of shared data between threads is a recipe for race 
conditions, deadlocks, starvation, and all the other attendant issues 
of multi-threaded code.

If we implement `produce` and `consume` as coroutines, however, we avoid
the pains of multithreading. `produce` simply gets some data and yields 
to `consume`. `consume` processes the data and yields control back 
to `produce`, waiting until more data is available. 

Two interesting things to note here. Only one coroutine is executing at any
time, so data sharing issues dissapear. Also, the execution pattern 
of `consume` is the basis for a large number of asynchronous IO frameworks.
Like `consume`, work is done until some resource is required, at which point
the coroutine yields.

<a id="coro"></a>
### Coroutines, Asynchronous I/O, and Cooperative Multitasking

The 

[^1]: A refresher: a prime number is a positive integer greater than 1
    that has no divisors other than 1 and itself. 3 is prime because there are no
    numbers that evenly divide it other than 1 and 3 itself.*

