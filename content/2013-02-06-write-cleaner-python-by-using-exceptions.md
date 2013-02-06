title: Write Cleaner Python: Use Exceptions
date: 2013-02-06 14:36
categories: python idioms exceptions

Many programmers have had it drilled into their head that exceptions, in any 
language, should only be used in truly exceptional cases.  They're wrong. 
The Python community's approach to exceptions leads to cleaner code that's
easier to read. And that's without the monstrous hit to performance commonly
associated with exceptions in other languages. 

## LBYL vs. EAFP

The difference of opinion regarding when (not if) to use exceptions
boils down to a tension between coding styles. Code that doesn't use
exceptions is always checking if it's OK to do something.

## Slow is relative

The fact that this schism exists is understandable. In a number of other 
languages (especially compiled ones), exceptions are comparatively expensive.
In this context, avoiding exceptions in performance sensitive code is 
reasonable. 

But this argument doesn't hold weight for Python. There is *some* overhead,
of course, to using exceptions in Python. *Comparatively*, though, it's
negligible in almost all cases. And I'm playing it safe by including "almost"
in the previous sentence.

Want proof? Regardless, here's some proof. To get an accurate sense of the
overhead of using exceptions, we need to measure two (and a half) things: 

1. The overhead of simply adding a `try` block but never throwing an exception
1. The overhead of using an exception vs. comparable code without exceptions
    1. When the exception case is quite likely
    1. When the exception case is unlikely

The first is easy to measure. We'll time two code blocks using the `timeit`
module. The first will simply increment a counter. The second will do the same
but wrapped in a `try`/`except` block.

Here's the script to calculate the timings:

    #!py
    SETUP = 'counter = 0'

    LOOP_IF = """
    counter += 1
    """

    LOOP_EXCEPT = """
    try:
        counter += 1
    except:
        pass
    """


    if __name__ == '__main__':
        import timeit
        if_time = timeit.Timer(LOOP_IF, setup=SETUP)
        except_time = timeit.Timer(LOOP_EXCEPT, setup=SETUP)
        print('using if statement: {}'.format(min(if_time.repeat(number=10 ** 7))))
        print('using exception: {}'.format(min(except_time.repeat(number=10 ** 7))))

Note that `Timer.repeat(repeat=3, number=1000000)` returns the time
taken to execute the code block `number` times, repeated `repeat` times. The
[Python documentation](http://docs.python.org/2/library/timeit.html) suggests
that the time should be at least 0.2 to be accurate, hence the change to `number`.  
The code prints the best run of executing each code block (`LOOP_IF` and `LOOP_EXCEPT`) 
10,000,000 times.

Clearly, all we're measuring here is the setup cost of using an exception. Here
are the results:

    #!bash
    >>> python exception_short
    using if statement: 0.574051856995
    using exception: 0.821137189865

So the presence of an exception increases run time by .3 seconds divided by
10,000,000. In other words: **if using a simple exception drastically impacts
your performance, you're doing it wrong...**

So an exception that does nothing is cheap. Great. What about one that's
actually useful? To test this, we'll load the words file found at
`/usr/share/dict/words` on most flavors of Linux. Then we'll conditionally 
increment a counter based on the presence of a random word. Here is the new 
timing script:

    #!py
    import timeit

    SETUP = """
    import random
    with open('/usr/share/dict/words', 'r') as fp:
        words = [word.strip() for word in fp.readlines()]
    percentage = int(len(words) *.1)
    my_dict = dict([(w, w) for w in random.sample(words, percentage)])
    counter = 0
    """

    LOOP_IF = """
    word = random.choice(words)
    if word in my_dict:
        counter += len(my_dict[word])
    """

    LOOP_EXCEPT = """
    word = random.choice(words)
    try:
        counter += len(my_dict[word])
    except KeyError:
        pass
    """


    if __name__ == '__main__':
        if_time = timeit.Timer(LOOP_IF, setup=SETUP)
        except_time = timeit.Timer(LOOP_EXCEPT, setup=SETUP)
        number = 1000000
        min_if_time = min(if_time.repeat(number=number))
        min_except_time = min(except_time.repeat(number=number))

        print """using if statement:
        minimum: {}
        per_lookup: {}
        """.format(min_if_time, min_if_time / number)

        print """using exception:
        minimum: {}
        per_lookup: {}
        """.format(min_except_time, min_except_time / number)

The only thing of note is the `percentage` variable, which essentially dictates
how likely our randomly chosen `word` is to be in `my_dict`. 

So with a 90% chance of an exception being thrown, here are the numbers:

    using if statement:
        minimum: 1.35720682144
        per_lookup: 1.35720682144e-06
 
    using exception:
        minimum: 3.25777006149
        per_lookup: 3.25777006149e-06

Wow! 3.2 seconds vs 1.3 seconds! Exceptions are teh sux0rz!

If you run them 1,000,000 times in a tight loop with a 90% chance of throwing
an exception, then exceptions are a bit slower, yes. Does any code you've 
*ever* written do that? No? Good, let's see a more realistic scenario.

Changing the chance of an exception to 20% gives the following result:

    using if statement:
        minimum: 1.49791312218
        per_lookup: 1.49791312218e-06

    using exception:
        minimum: 1.92286801338
        per_lookup: 1.92286801338e-06

At this point the numbers are close enough to not care. A differnce of 0.5 \* 10^6
seconds shouldn't matter to anyone. If it does, I have a spare copy of the K&R C
book you can have; go nuts.

What did we learn?

**Exceptions in Python are not "slow".**


