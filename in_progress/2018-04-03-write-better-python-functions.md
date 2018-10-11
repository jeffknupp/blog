title: Write Better Python Functions
date: 2018-04-03 09:34
categories: python function

In Python, like most modern programming languages, the *function* is a primary method of abstraction and encapsulation. You've probably written hundreds of functions in your time as a developer. But not all functions are created equal. And writing "bad" functions directly affects the readability and maintainability of your code. So what, then, is a "bad" function and, more importantly, what makes a "good" function?

<!--more-->

## A Quick Refresher

Math is lousy with functions, though we might not remember them, so let's think back to everyone's favorite topic: calculus. You may remember seeing formulas like the following `f(x) = 2x + 3`. This is a function, called `f`, that takes an argument `x`, and "returns" two times `x` + 3. While it may not look like the functions we're used to in Python, this is directly analagous to the following code:

```py
    def f(x):
        return 2*x + 3
```

Functions have long existed in math, but have far more power in computer science. With this power, though, comes various pitfalls. Let's now discuss what makes a "good" function and warning signs of functions that may need some refactoring.

## Keys To A Good Function

What differentiates a "good" Python function from a crappy one? You'd be surprised at how many definitions of "good" one can use. For our purposes, I'll consider a Python function "good" if it can tick off *most* of the items on this checklist (some are not always possible): 

* Sensibly named
* Has a single responsibility
* Includes a docstring
* Returns a value
* Is *idempotent* and, if possible, *pure*
* Is no longer than 50 lines

For many of you, this list may seem overly draconian. I promise you, though, if your functions follow these rules, your code will be so beautiful it will make
unicorns weep.

Below, I'll devote a section to each of the items, then wrap things up with how they work in harmony to create "good" functions.

### Naming

There's a favorite saying of mine on the subject, often misatributed to Donald Knuth, but which actually came from [Phil Karlton](https://martinfowler.com/bliki/TwoHardThings.html):

    There are only two hard things in Computer Science: cache invalidation and naming things.

    -- Phil Karlton

As silly as it sounds, naming things well *is difficult*. Here's an example of a "bad" function name:

    ```py

    def get_knn_from_df(df):

    ```

Now, I've seen bad names literally everywhere, but this example comes from Data Science (really, Machine Learning), where its practitioners typically write code in Jupyter notebooks and later try to turn those various cells into a comprehensible program.

The first issue with the name of this function is its use of acronyms/abbreviations. **Prefer full English words to abbreviations and non-universally known acronyms.** The only reason one might abbreviate words is to save typing, but *every modern editor has autocomplete*, so you'll only be typing that full name once. Abbreviations are an issue because they are often domain specific. In the code above, `knn` refers to "K-Nearest Neighbors", and `df` refers to "DataFrame", the ubiquitous [pandas](https://pandas.pydata.org/) data structure. If another programmer not familiar with those acronyms is reading the code, almost nothing about the name will be comprehensible to her.

There are two other minor gripes about this function's name: the word "get" is extraneous. For most well-named functions, it will be clear that something is being returned from the function, and its name will reflect that. The `from_df` bit is also unneccessary. Either the function's docstring or (if living on the edge) type annotation will describe the type of the parameter *if it's not already made clear by the parameter's name*.

So how might we rename this function? Simple:

    ```py

    def k_nearest_neighbors(dataframe):

    ```

It is now clear even to the lay person what this function calculates, and the parameter's name (`dataframe`) makes it clear what type of argument should be passed to it.

### Single Responsibility

Straight from "Uncle" Bob Martin, the [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single_responsibility_principle) applies just as much to functions as it does classes and modules (Mr. Martin's original targets). It states that (in our case) a function should have a *single responsibility*. That is, it should do one thing and *only* one thing. One great reason is that if every function only does one thing, there is only one reason ever to change it: if the way in which it does that thing must change. It also becomes clear when a function can be deleted: if, when making changes elsewhere, it becomes clear the function's single responsibility is no longer needed, simply remove it.

An example will help. Here's a function that does more than one "thing":

    ```py

    def calculate_and print_stats(list_of_numbers):
        sum = sum(list_of_numbers)
        mean = statistics.mean(list_of_numbers)
        median = statistics.median(list_of_numbers)
        mode = statistics.mode(list_of_numbers)

        print('-----------------Stats-----------------')
        print('SUM: {}'.format(sum)
        print('MEAN: {}'.format(mean)
        print('MEDIAN: {}'.format(median)
        print('MODE: {}'.format(mode)

    ```

This function does *two* things: it calculates a set of statistics about a list of numbers *and* prints them to `STDOUT`. The function is in violation of the rule that there should be only one reason to change a function. There are two obvious reasons this function would need to change: new or different statistics might need to be calculated or the format of the output might need to be changed. This function is better written as two separate functions: one which performs and returns the results of the calculations and another that takes those results and prints them. *One dead giveaway that a function has multiple responsibilties is the word **and** in the functions name.*

This separation also allows for much easier testing of the function's behavior and also allows the two parts to be separated not just into two functions in the same module, but possibly live in different modules altogether if appropriate. This, too, leads to cleaner testing and easier maintenance.

Finding a function that only does *two* things is actually rare. Much more often, you'll find functions that do many, many more things. Again, for readability and testability purposes, these jack-of-all-trade functions should be broken up into smaller functions that each encapsulate a single unit of work.

### Docstrings

While everyone seems to be aware of [PEP-8](https://www.python.org/dev/peps/pep-0008/), defining the style guide for Python, far fewer seem to be aware of [PEP-257](https://www.python.org/dev/peps/pep-0257/), which does the same for docstrings. Rather than simply rehash the contents of PEP-257, feel free to read it at your leisure. The main takeaways, however, are:

* *Every* function requires a docstring
* Use proper grammar and punctuation; write in complete sentences
* Begins with a one-sentence summary of what the function does
* Uses prescriptive rather than descriptive language

This is an easy one to tick off when writing functions. Just get in the habit of always writing docstrings, and try to write them *before* you write the code for the function. If you can't write a clear docstring describing what the function will do, it's a good indication you need to think more about why you're writing the function in the first place.

### Return Values

Functions can (and *should*) be thought of as little self-contained programs. They take some input in the form of parameters and return some result. Parameters are, of course, optional. *Return values, however, are not optional, from a Python internals perspective.* Even if you *try* to create a function that doesn't return a value, you can't. If a function would otherwise not return a value, the Python interpreter "forces it" to return `None`. Don't believe me? Test out the following yourself:

```

❯ python3
Python 3.7.0 (default, Jul 23 2018, 20:22:55)
[Clang 9.1.0 (clang-902.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> def add(a, b):
...   print(a + b)
...
>>> b = add(1, 2)
3
>>> b
>>> b is None
True

```

You'll see that the value of `b` really is `None`. So, even if you write a function with no `return` statement, it's still going to return *something*. And it *should* return something. After all, it's a little program, right. How useful are programs that produce no output, including whether or not they executed correctly? But most importantly, how would you *test* such a program?

I'll even go so far as to make the following statement: every function should return a useful value, even if only for testability purposes. Code that you write should be tested (that's not up for debate). Just think of how gnarly testing the `add` function above would be (hint: you'd have to redirect I/O and things go south from there quickly). Also, returning a value allows for method chaining, a concept that allows us to write code like this:

```

with open('foo.txt', 'r') as input_file:
    for line in input_file:
        if line.strip().lower().endswith('cat'):
            # ... do something useful with these lines

```

The line `if line.strip().lower().endswith('cat'):` works because each of the string methods (`strip(), lower(), endswith()`) *return a string as the result of calling the function.*

Here are some common reasons people give when asked why a given function they wrote doesn't return a value:

##### "All it does is [some I/O related thing like saving a value to a database]. I can't return anything useful."

I disagree. The function can return `True` if the operation completed successfully.

##### "We modify one of the parameters in place, using it like a reference parameter."""

Two points, here. First, do your best to avoid this practice. For others, providing something as an argument to your function only to find that it has been changed can be surprising in the best case and downright dangerous in the worst. Instead, much like the string methods, prefer returning a new instance of the parameter with the changes applied to it. Even when this isn't feasible because making a copy of some parameter is prohibitively expensive, you can still fall back to the old "Return `True` if the operation completed successfully" suggestion.

##### "I need to return multiple values. There is no single value I could return that would make sense."

This is a bit of a strawman argument, but I *have* heard it. The answer, of course, is to do exactly what the author wanted to do but didn't know how to do: *use a tuple to return more than one value.*

And perhaps the most compelling argument for always returning a useful value is that callers are always free to ignore them. In short, returning a value from a function is almost certainly a good idea and very unlikely to break anything, even in existing codebases.

### Idempotency and Functional Purity

The title of this subsection may sound a bit intimidating, but the concepts are simple. An *idempotent* function always returns the same value given the same set of arguments, regardless of how many times it is called. The result does not depend on non-local variables, the mutability of arguments, or any I/O streams. The following `add_three(number)` function is idempotent:

```

def add_three(number):
    """Return *number* + 3."""
    return number + 3

```

No matter how many times one calls `add_three(7)`, the answer will always be `10`. Here's a different take on the function that **is not** idempotent:

```

def add_three():
    """Return 3 + the number entered by the user."""
    number = int(input('Enter a number: '))
    return number + 3

```

This admitedly contrived example is not idempotent because the return value of the function depends on I/O, namely the number entered by the user. It's clearly not true that every call to `add_three()` will return the same value. If it is called twice, the user could enter `3` the first time and `7` the second, making the call to `add_three()` return `6` and `10`, respectively.

A real-world example of idempotency is hitting the "up" button in front of an elevator. The first time it's pushed, the elevator is "notified" that you want to go up. Because the pressing the button is idempotent, pressing it over and over again is harmless. The result is always the same.

##### Why is idempotency important

**Testability and maintainability.** Idempotent functions are
