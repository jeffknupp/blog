Prior to beginning tutoring sessions, I ask new students to fill out a brief
questionaire about their understanding of various Python concepts. Some 
topics ("control flow with if/else" or "defining and using functions") are 
understood by a majority of students before beginning tutoring. There are a
handful of topics, however, that almost all students report having no
knowledge/limited understanding of. Of these, the `generators` and the `yield` 
keyword is one of the biggest culprits. I'm guessing this is the case for most 
novice Python programmers.

Many report having difficulty understanding `generators` and the `yield` 
keyword even after making a concerted effort to teach themselves the topic.
I want to change that. In this post, I'll explain *what* the `yield` 
keyword does, *why* it's useful, and *how* to use it.

*Note: In recent years, generators have grown more powerful as features have beend added through PEPs. In an upcoming post, I'll explore the true power of `yield` with respect to coroutines, cooperative multitasking and asynchronous I/O (especially their use in the ["tulip"](https://code.google.com/p/tulip/) prototype implementation GvR has been working on). Before we get there, however, we need a solid understanding of how the `yield` keyword and `generators` work.* 

## Coroutines and Subroutines

When we call a normal Python function, execution starts at function's first line
and continues until a `return` statement, `exception`, or the end of the
function (which is seen as an implicit `return None`) is encountered.
Once a function returns control to it's caller, that's it. Any work done by the
function and stored in local variables is lost. A new call to the function
creates everything from scratch.

This is all very standard when discussing functions (more generally refferred to as [subroutines](http://en.wikipedia.org/wiki/Subroutine)) in
computer programming. There are times, though, when it's beneficial to have
the ability to create a "function" which, instead of simply returning a single
value, is able to yield a series of values. To do so, such a function would need
to be able to "save it's work," so to speak.

I said, "yield a series of values" because our hypothetical function 
doesn't "return" in the normal sense. `return` implies that the function 
is *returning control of execution* to the point where the function was called. 
"Yield," however, implies that *the transfer of control is temporary and voluntary*, 
and our function expects to regain it in the future.

In Python, "functions" with these capabilities are called `generators`, and 
they're incredibly useful. `generators` (and the `yield` statement) were initially introduced to give 
programmers a more straightforward way of writing code that produced a series of
values. Previously, creating something like a random number generator required
a class or module that both generated values and kept track of state between calls. 
With the introduction of `generators`, this became much simpler.

To better understand the problem `generators` solve, let's take a look at an 
example. Throughout the example, keep in mind the core problem being solved:
**generating a series of values.**

*Note: Outside of Python, all but the simplest `generators` would be referred to as [`coroutines`](http://en.wikipedia.org/wiki/Coroutine). I'll use the latter term later in the post. The important thing to remember is, in Python, everything described here as a `coroutine` is still a `generator`. Python formally defines the term `generator`; `coroutine` is used in discussion but has no formal definition in the language.*

### Example: Fun With Prime Numbers

Suppose our boss asks us to write a function that takes a `list` of `int`s and 
returns some Iterable containing the elements which are prime numbers [^prime].

*Remember, an [Iterable](http://docs.python.org/3/glossary.html#term-iterable) is just an object capable of returning its members one at a time.*

"Simple," we say, and we write the following:

    #!py
    def get_primes(input_list):
        result_list = list()
        for element in input_list:
            if is_prime(element):
                result_list.append()
    
    # or better yet...

    def get_primes(input_list):
        return (element for element in input_list if is_prime(element))

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
boss we're done. She reports our function works and is exactly what she wanted.

#### Dealing With Infinite Sequences

Well, not quite *exactly*. A few days later, our boss comes back and tells 
us she's run into a small problem: she wants to use our `get_primes` function on a
very large list of numbers. In fact, the list is so large that merely creating 
it would consume all of the system's memory. To work around this, she wants to be 
able to call `get_primes` with a `start` value and get all the primes 
larger than `start` (perhaps she's solving [Project Euler problem 10](http://projecteuler.net/problem=10)).

Once we think about this new requirement, it becomes clear that it requires 
more than a simple change to `get_primes`. Clearly, we can't return a 
list of all the prime numbers from `start` to infinity. *(operating on infinite sequences, though, has a wide range of useful applications)*. 
The chances of solving this problem using a normal function seem bleak.

Before we give up, let's determine the core obstacle preventing us 
from writing a function that satisfies our boss's new requirements.
Thinking about it, we arrive at the following: *functions only get 
one chance to return results, and thus must return all results at once.*
It seems pointless to make such an obvious statement; "functions just
work that way," we think. The real value lies in asking, "but what if they
didn't?"

Imagine if `get_primes` could simply return the *next* value
instead of all the values at once. It wouldn't need to create
a list at all. No list, no memory issues. Since our boss told 
us she's just iterating over the results, she wouldn't know 
the difference.

Unfortunately, this doesn't seem possible. Even if we had a 
magical function that allowed us to iterate from `n` to `infinity`, we'd 
get stuck after returning the first value:

    #!py
    def get_primes(start):
        for element in magical_infinite_range(start):
            if is_prime(element):
                return element

Imagine `get_primes` is called like so:

    #!py

        def solve_number_10():
            # She *is* working on Project Euler #10, I knew it!
            total = 2
            for next_prime in get_primes(3):
                if next_prime < 2000000:
                    total += next_prime
                else:
                    print(total)
                    return

Clearly, in `get_primes`, we would hit the number `3` and return at line 4.
Instead of `return`, we need a way to generate a value and, when asked for 
the next one, pick up where we left off.

Functions, though, can't do this. When they `return`, they're
done for good. Even if we could guarantee a function would be called again, we
have no way of saying, "OK, now, instead of starting at the first line like
we normally do, start up where we left off at line 4." Functions have a single `entry
point`: the first line.

## Enter Generators

This sort of problem is so common that a new concept was added to Python
to help solve it: the `generator`. A `generator` "generates" values. To make creating
generators as straightforward as possible, `generator functions` were introduced as well.
A `generator function` is defined like a normal function, but whenever it needs to generate a
value, it does so with the `yield` keyword rather than `return`. If the body of a `def` 
contains `yield`, it automatically becomes a `generator function` (even if it
also contains a `return` statement). There's nothing else we need to do to create one. 

`generator functions` create `generator iterators`. That's the last time 
you'll see the term `generator iterator`, though, since they're almost
always refferred to as "`generators`". Just remember that a `generator`
is a special type of `iterator`. To be considered an `iterator`, `generators` 
must define a few methods, one of which is `__next__()`. 

**To get the next value from a `generator`, we use the same built-in function as
for `iterators`: `next()`.** 
    
(`next()` takes care of calling the generator's `__next__()` method). Since a
`generator` is a type of `iterator`, it can be used in a `for` loop.

So whenever `next()` is called on a `generator`, the `generator` is responsible
for passing back a value to whomever called `next()`. It does so by calling `yield`
along with the value to be passed back (e.g. `yield 7`). 

**`yield` is just `return` (plus a little magic) for `generator functions`.**

Here's a simple `generator function`:

    def simple_generator_function():
        yield 1
        yield 2
        yield 3

And here are two simple ways to use it:

    #!py
    our_generator = simple_generator_function()
    print(next(our_generator))
    >>> 1
    print(next(our_generator))
    >>> 2
    print(next(our_generator))
    >>> 3
    

What's the magic part? Glad you asked! When a `generator function` calls `yield`, 
the "state" of the `generator function` is frozen; the values of all variables and the next line of code to be
executed are recorded. To get the next value from a `generator`, we call `next()` 
on it (or let a `for` loop do it for us automatically).
If `yield` is called with a value, as in `yield 7`, the value is
returned to the caller 
Let's rewrite our `get_primes` function as a `generator function`. We no longer need 
the `magical_infinite_range` function. Since `generator functions` "remember" both where
they left off *and* the values of their variables, we can create our own infinite
sequence:

    #!py
    def get_primes(number):
        while True:
            if is_prime(number):
                yield number
            number += 1



It's helpful to visualize how the first few elements are created when we call
`get_primes` in `solve_number_10`'s `for` loop. When the `for` loop requests the first `next_prime`, 
we enter `get_primes` as we would in a normal function: from the first line. 
We enter the `while` loop, the `if` condition holds (`3` is prime) so we yield 
the value `3` and control to ` solve_number_10`.  The `for` loop then requests 
the next element from `get_primes`. Instead of starting back at the top, we 
resume at line 5, where we left off.


    #!py
    def get_primes(number):
        while True:
            if is_prime(number):
                yield number
            number += 1 <<<<<<<<<<

Most importantly, `number` *still has the same value it did when we called `yield`*
(i.e. `3`). Clearly, then, `number` is incremented to `4`, we hit the top of the `while` loop, and 
keep incrementing `number` until we hit the next prime number (`5`). Again we `yield` the 
value of `number` to the `for` loop in `solve_number_10`. This continues until the `for` loop
stops (at the first prime greater than `2,000,000`).

Note that, when we invoke a `generator function` directly, a `generator object` is returned.
This means, just like with iterators, we are free to assign the result of a `generator
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

*By doing so, [PEP 342](http://www.python.org/dev/peps/pep-0342/) effectively allowed a generator to call other functions
or generators without blocking. This gave `yield` the power to create proper
`coroutines`.  More on this later.*

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

