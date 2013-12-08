title: Improve Your Python: Understanding Unit Testing
date: 2013-12-08 09:14
categories: python testing unit-testing improveyourpython

One frequent source of confusion for novice developers is the subject of
testing. They are vaugely aware that "unit testing" is something that's good 
and that they should do, but don't understand what the term actually means. If
that sounds like you, fear not! In this article, I'll describe what `unit testing`
is, why it's useful, and how to `unit test` Python code.

## What is Testing?

Before discussing *why* testing is useful and *how* to do it, let's take a
minute to define *what* `unit testing` actually is. "Testing", in general programming
terms, is the practice of writing code (separate from your actual application
code) that invokes the code it tests to help determine if there are any
errors. It **does not** prove that code is correct (which is only possible under
very restricted circumstances). It merely if the conditions the tester thought
of are handled correctly.

*Note: when I use the term "testing", I'm always referring to "automated testing", where the tests are run by the machine. "Manual testing", where a human runs the program and interacts with it to find bugs, is a separate subject.* 

What kinds of things can be caught in testing? **Syntax errors** are
unintentional misuses of the language, like the extra `.` in
`my_list..append(foo)`. **Logical errors** are created when the algorithm (which
can be thought of as "the way the problem is solved") is not correct. Perhaps the programmer
forgot that Python is "zero-indexed" and tried to print the last character in a
string by writing `print(my_string[len(my_string)])` (which will cause an
`IndexError` to be raised). Larger, more systemic errors can also be checked for. 
Perhaps the program always crashes when the user inputs a number greater 
than `100`, or hangs if the web site it's retrieving is not available. 

All of these errors can be caught through careful testing of the code. `Unit
testing`, specifically tests a single "unit" of code **in isolation**. A `unit`
could be an entire module, a single class or function, or almost anything in between.
What's important, however, is that the code is isolated from *other* code we're
not testing (which itself could have errors and would thus confuse test results). 
Consider the following example:

    #!py

    def is_prime(number):
        """Return True if *number* is prime."""
        for element in range(number):
            if number % element == 0:
                return False

        return True

    def print_next_prime(number):
        """Print the closest prime number larger than *number*."""
        index = number
        while True:
            index += 1
            if is_prime(index):
                print(index)

We have two functions, `is_prime` and `print_next_prime`. If we wanted to test
`print_next_prime`, we would need to be sure that `is_prime` is correct, as
`print_next_prime` makes use of it. In this case, the function
`print_next_prime` is one unit, and `is_prime` is another. Since `unit tests`
test only a **single** unit at a time, we would need to think carefully about
how we could accurately test `print_next_prime` (more on how this is
accomplished later).

So what does test code look like? If the previous example is stored in a file
named `primes.py`, we may write test code in a file named `test_primes.py`.
Here are the minimal contents of `test_primes.py`, with an example test:

    #!py
    import unittest
    from primes import is_prime

    class PrimesTestCase(unittest.TestCase):
        """Tests for `primes.py`."""

        def test_is_five_prime(self):
            """Test that five is successfully considered prime."""
            self.assertTrue(is_prime(5))

    if __name__ == '__main__':
        unittest.main()

The file creates a `unit test` with a single `test case`: `test_is_five_prime`.
Using Python's built-in `unittest` framework, any member function whose name begins
with `test` in a class deriving from `unittest.TestCase` will be run, and its
assertions checked, when `unittest.main()` is called. If we "run the tests" by
running `python test_primes.py`, we'll see the output of the `unittest`
framework printed on the console:

    #!bash
    $ python test_primes.py
    E
    ======================================================================
    ERROR: test_is_five_prime (__main__.PrimesTestCase)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "test_primes.py", line 8, in test_is_five_prime
        self.assertTrue(is_prime(5))
    File "/home/jknupp/code/github_code/blug_private/primes.py", line 4, in is_prime
        if number % element == 0:
    ZeroDivisionError: integer division or modulo by zero

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

The single "E" represents the results of our single test (if it was successful,
a "." would have been printed). We can see that our test failed, the line that
caused the failure, and any exceptions raised.

## Why Testing?

Before we continue with the example, it's important to ask the question, "Why is testing
a valuable use of my time?" It's a fair question, and it's the question those
unfamiliar with testing code often ask. After all, testing takes time that could
otherwise be spend writing code, and isn't that the most productive thing to be
doing?

There are a number of valid answers to this question. I'll list a few here:

#### Testing makes sure your code works properly under a given set of conditions

Testing assures correctness under a basic set of conditions. Syntax errors will
almost certainly be caught by running tests, and the basic logic of a unit of
code can be tested to ensure correctness under certain conditions. Again, it's
not about proving the code is correct *under any set of conditions*. We're
simply aiming for a reasonably complete set of possible conditions (i.e. you may
write a test for what happens when you call `my_addition_function(3,
'refrigirator`), but you needn't test all possible strings for each argument).

#### Testing allows one to ensure that changes to the code did not break existing functionality
    
This is especially helpful when `refactoring`[^1] code. Without tests in place,
you have no assurances that your code changes did not break things that were
previously working fine. **If you want to be able to change or rewrite your code and know you didn't break anything, proper unit testing is imperative.**

#### Testing forces one to think about the code under unusual conditions, possibly revealing logical errors

Writing tests forces you to think about the non-normal conditions your code may
encounter. In the example above, `my_addition_function` adds two numbers. A
simple test of basic correctness would call `my_addition_function(2, 2)` and
assert that the result was `4`. Further tests, however, might test that the
function works correctly with `float`s  by running `my_addition_function(2.0, 2.0)`. 
*Defensive coding* principles suggest that your code should be able to
gracefully fail on invalid input, so testing that an exception is properly raised
when strings are passed as arguments to the function.

#### Good testing requires modular, decoupled code, which is a hallmark of good system design

The whole practice of unit testing is made much easier by code that is *loosely coupled*[^2]
  

[^1] Reorganizing/cleaning up code without changing functionality
[^2] Code that does not expose its internal data or functions and does not make use of the internal data or functions of other code
