
There are a handful of topics that Python novices find a bit confusing. Three
stand out as the most common: Generators, Decorators, and Class and Metaclass
magic. This is the first in a series of posts that explain the concepts, why
they're useful, and how (and when/if) to use them.

##Understanding `yield` and Generators

When we call a normal Python function, the code starts at the first line of the
function and executes until it hits a `return` statement, an `exception` is
thrown, or there are no more lines to execute (in which case it returns `None`).

Let's look at an example. Suppose our boss asks us to write
a function that takes a `list` of `int`s and returns all the elements which are
prime numbers TODO asdf!!!!(^prime]. He's just going to print them out in a nicely
formatted manner, so we're free to return the results as anything that he can
use in a `for` loop.

    #!py
    import math

    def get_primes(input_list):
        result_list = list()
        for element in input_list:
            if element > 1 and is_prime(element):
                result_list.append()

    def is_prime(number):
    if number > 1:
        if number % 2 == 0:
            return False
        for current in range(3, number, 2):
            if number % current == 0: 
                return False
        return True
    return False

This function fulfills the requirements, so we can safely tell our boss we're done.

# Infinite sequences

Our boss comes back after a couple of days and tells us our function is working
great, but there's a problem: he wants to use our `get_primes` function on a
very large list of numbers, but merely creating that list would use too much memory.
In fact, he want to be able to call `get_primes` with just a `start` value and
get all the primes larger than that number, like calling `range()` with no end
point.

This is obviously not a simple change to `get_primes`. Operating over infinite
sequences, though, is a useful thing to be able to do. In `get_primes`,
it would be nice if instead of returning all of the values, we could 
just return the *next* value. Then we're not creating a list at all and, thus,
we avoid the memory issue.  And because our boss told us he's just iterating 
over the results, he wouldn't know the difference. 

But that doesn't seem possible. Even if we had a magical function that we could
iterate over from `n` to `infinity`, we'd get stuck after returning the first
value:

    #!py
    def get_primes(start):
        for element in magical_infinite_range(start):
            if element > 1 and is_prime(element):
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
temporarily suspend work in `get_primes` and return `5`, with the understanding
that when the next `element` is requested by the `for` loop, we will resume
where we left off. 

Functions, though, can't do this. When they `return`, they're
done for good. Even if we could guarantee a function would be called again, we
have no way of saying, "OK, now, instead of starting at the first line like
we normally do, start up where we left off at line 4." Functions have a single entry
point: the first line.

Luckily, Python has a tool designed to solve this exact problem:
**`Generators`**.

A `generator` looks like a normal function, but whenever we need to generate a
value, we call `yield` instead of `return`. Those names are quite
descriptive. `yield` implies "I am voluntarily giving up control for a while,"
while `return` basically says, "Return to wherever you were before you called
me."

To write our `get_primes` function as a `generator`, we first need a way to
operate on an infinite sequence. A `generator` is the key here, as well:

    #!py
    def magical_infinite_range(start=0):
        while True:
            yield start
            start += 1

The `yield start` line essentially says, "give the value `start` to whomever
called me and let them run until they need the next element. When they do, they give control
back to me and let me run from where I left off." 

It's helpful to visualize how the first few elements are created when we call
`magical_infinite_range` in a `for` loop.

    #!py
    def magical_infinite_range(start=0):
        while True:
            yield start
            start += 1

    for element in magical_infinite_range(5):
        print(element)

For the first element, we enter `magical_infinite_range` as we would in a
function: we enter the `while` loop. When we hit the next line, `yield start`,
we give back the value of start (`5`) and yield control to the `for` loop. 

The `for` loop then requests the next element from `magical_infinite_range`.
Instead of at the top, we resume at line 4, where we left off.

    #!py
    def magical_infinite_range(start=0):
        while True:
            yield start
            start += 1  # <<<<<<<<<

Most importantly, `start` has the same value it did when we called `yield`
(`5`). So `start` is incremented to `6`, we hit the top of the `while` loop, and we
again `yield` the value of `start` (`6`) to the `for` loop. Subsequent values
are produced in the same way.


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

[^1]: A refresher: a prime number is a positive integer greater than 1
    that has no divisors other than 1 and itself. 3 is prime because there are no
    numbers that evenly divide it other than 1 and 3 itself.*

