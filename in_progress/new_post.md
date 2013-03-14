
There are a handful of topics that Python novices find a bit confusing. Three
stand out as the most common: Generators, Decorators, and Class and Metaclass
magic. This is the first in a series of posts that explain the concepts, why
they're useful, and how (and when/if) to use them.

##Understanding `yield` and Generators

When we call a normal Python function, the code starts at the first line of the
function and executes until it hits a `return` statement, an `exception` is
thrown, or there are no more lines to execute (in which case it returns `None`).
Once a function returns control to it's caller, that's it. The values calculated
while the function executed are destroyed, as is the location the function
exited from. 

This is all very standard when discussing functions (or *subroutines*) in most
programming languages. There are times, though, when it's beneficial to have
functions that can do something, yield a value, then later resume where
they left off. I say "yield a value" because they dont't "returning" the value.
`return` implies that the function is "returning" execution to the point at
which it was called. "Yield," however, implies that the transfer of control is
temporary, and the function expects to regain it in the future.

"Functions" with these capabilites are called `coroutines`, and they're
incredibly useful. Consider the following example where the main issue is one of
controlling iteration: 

Suppose our boss asks us to write a function that takes a `list` of `int`s and 
returns all the elements which are prime numbers TODO asdf!!!!(^prime]. The only
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

    def is_prime(number):
    if number > 1:
        if number % 2 == 0:
            return False
        for current in range(3, number, 2):
            if number % current == 0: 
                return False
        return True
    return False

Either implementation fulfills the requirements, so we tell our boss we're done.

# Infinite sequences

Our boss comes back after a couple of days and tells us our function is working
great, but there's a problem: he wants to use our `get_primes` function on a
very large list of numbers. In fact, the list is so large that merely creating 
it would use all the memory on the system. He wants to be able to 
call `get_primes` with a `start` value and get all the primes larger than `start`.

This is obviously not a simple change to `get_primes`. Operating on infinite
sequences, though, is a generally useful thing to be able to do. In `get_primes`,
it would be nice if instead of returning all of the values, we could 
just return the *next* value. Then we're not creating a list at all and, thus,
avoid the memory issue. And because our boss told us he's just iterating 
over the results, he wouldn't know the difference. 

But that doesn't seem possible. Even if we had a magical function that we could
iterate over from `n` to `infinity`, we'd get stuck after returning the first
value:

    #!py
    def get_primes(start):
        for element in magical_infinite_range(start):
            if is_prime(element):
                return element

Imagine `get_primes` is called like so:

    #!py
    for prime in get_primes(10):
        print(prime)
        # should stop is determined by the user
        if should_stop():
            break

In our code, we would hit the number `5` and return at line 4 of `get_primes`. 
But what about generating the next value? Instead of `return`, we need a way to
return an "intermediate" value and, when asked for next prime, pick up where 
we left off.

Functions, though, can't do this. When they `return`, they're
done for good. Even if we could guarantee a function would be called again, we
have no way of saying, "OK, now, instead of starting at the first line like
we normally do, start up where we left off at line 4." Functions have a single entry
point: the first line.

Luckily, Python has a tool designed to solve this exact problem:
**`Generators`**.

A `generator function` looks like a normal function, but whenever we need to generate a
value, we call `yield` instead of `return`. Those names are quite
descriptive. `yield` implies "I am voluntarily giving up control for a while,"
while `return` basically says, "Return to wherever you were before you called
me."

When we write our `get_primes` function as a `generator`, we no longer need 
the `magical_infinite_range` function. Since generators "remember" both where
they left off *and* the values of variables, we can create our own infinite
sequence:

    #!py
    def get_primes(start):
        while True:
            if is_prime(start):
                yield start
            start += 1


It's helpful to visualize how the first few elements are created when we call
`get_primes` in a `for` loop.

    #!py

    for element in get_primes(4):
        print(element)

For the first element, we enter `get_primes` as we would in a
function: we enter the `while` loop. The `if` condition doesn't hold (4 isn't
prime) so we add 1 to `start`. The next time through, the `if` condition *does*
hold, so we give back the value of start (`5`) and yield control to the `for` loop. 

The `for` loop then requests the next element from `get_primes`.
Instead of starting back at the top, we resume at line 5, where we left off.

    #!py
    def get_primes(start):
        while True:
            if is_prime(start):
                yield start
            start += 1 <<<<<<<<<

Most importantly, `start` has the same value it did when we called `yield`
(`5`). So `start` is incremented to `6`, we hit the top of the `while` loop, and 
keep incrementing start until we hit the next prime (`7`). Again we `yield` the 
value of `start` to the `for` loop. Subsequent values are produced in the same way.


Any time a `def` contains a `yield` statement, the result is changed from a
normal function to a `generator function`. `generator function`s automatically
define a few methods, one of which is `next()`. Since any object defining a
`next` function can be iterated over, we're able to use our `generator function`
in a `for` loop.

It should now be clear how we can implement `get_primes`. Like
`magical_infinite_range`, we'll create a `generator function` and simply `yield` 
each value in turn:

    #!py
    def get_primes(start):
        for element in magical_infinite_range(start):
            if is_prime(element):
                yield element

Note that, just like with iterators, we are free to assign a `generator
function` to a variable and call `next()` on it directly. The following would
print the first three primes:

    #!py
    generator = get_primes(3)
    print(generator.next())
    print(generator.next())
    print(generator.next())

### Communicating with a generator

The `yield` keyword can do more than just yield a value. It can also be used to
*set* a value at the same time. Instead of simply printing every prime number
greater than `start`, let's find the smallest prime number greater than
successive factors of 10 (that is, the smallest prime greater than 10, then 100,
then 1000, etc.). We start in the same way as `magical_infinite_range`:

    #!py
    def print_successive_primes(base=10, iterations):
        generator = get_primes(base)
        # missing code...
        for power in range(iterations):
            # missing code...

    def get_primes(start):
        while True:
            if is_prime(start):

The next line takes a bit of explanation. While `yield start` would yield the
value of start, the statement `other = (yield start)` means "yield `start` and,
if any value is sent to me, set `other` to that value." You can "send" values to
a generator using the generator's `send` method.

    #!py
    def get_primes(start):
        while True:
            if is_prime(start):
                start = (yield start)
            start += 1

In this way, we can set `start` to a different value each time the generator
`yield`s. We can now fill in the missing code in `print_successive_primes`:

    #!py
    def print_successive_primes(base=10, iterations):
        generator = get_primes(base)
        generator.send(None)
        for power in range(iterations):
            print(generator.send(base ** power))

Two things to note here: First, we're printing the result of `generator.send`,
which is possible because `send` both sends a value to the generator and 
returns the value yielded by the generator. 

Second, notice the `generator.send(None)` line. When you're using send to "start" a generator 
(that is, execute the code from the first line of the generator function up to
the first `yield` statement), you must send `None`. This makes sense, since by definition
the generator hasn't gotten to the first `yield` statement yet, so if we sent a
real value there would be nothing to "receive" it. Once the generator is started, we
can send values as we do above.



especially when more than one is involved. In a typical
producer/consumer implementation, we either need something in the 
middle to mediate (like the following):

    #!py
    def process_data():
        while True:
            items = produce()
            consume(items)

or we use a queue available to both `produce` and `consume`, each of which runs
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

Of course, the `Queue` must be synchronized because it represents data shared
between multiple threads. In the example above, it's straightforward (the
`Queue` class manages this internally), but more realistic uses of shared data
is a recipe for race conditions, deadlocks, starvation, and all the other
attendant issues of multi-threaded code.

If we implement `produce` and `consume` as coroutines, however, we avoid both
the pains of multithreading and the need for "central management". `produce`
simply gets some data and yields to `consume`. `consume` processes the data and 
yields control back to `produce`, waiting until more data is available. 

Two interesting things to note here. Only one coroutine is executing at any
time, so data sharing issues dissapear. Also, the execution pattern 
of `consume` is the basis for a large number of asynchronous IO frameworks.
Like `consume`, work is done until some resource is required, at which point
the coroutine yields.

[^1]: A refresher: a prime number is a positive integer greater than 1
    that has no divisors other than 1 and itself. 3 is prime because there are no
    numbers that evenly divide it other than 1 and 3 itself.*

