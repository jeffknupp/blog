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

What differentiates a "good" Python function from a crappy one? You'd be surprised at how many definitions of "good" one can use. For our purposes, I'll consider a Python function "good" if it can tick off the items on this checklist: 

* Sensibly named
* Has a single responsibility
* Includes a docstring
* Returns a value
* Is *idempotent*
* Is no longer than 50 lines

For many of you, this list may seem overly draconian. I promise you, though, if
your functions follow these rules, your code will be so beautiful it will make
unicorns weep.

Below, I'll devote a section to each of the items, then wrap things up with how
they work in harmony to create "good" functions.

### Naming

There's a favorite saying of mine on the subject, often misatributed to Donald Knuth, but which actually belongs to [Phil Karlton](https://martinfowler.com/bliki/TwoHardThings.html):

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

Straight from "Uncle" Bob Martin, the [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single_responsibility_principle) applies just as much to functions as it does classes and modules (Mr. Martin's original targets). It states that (in our case) a function should have a *single responsibility*. That is, it should do one thing and *only* one thing. One great reason is that if every function only does one thing, there is only one reason ever to change it: if the way in which it does that thing must change. It also becomes clear when a function is no longer neeeded if, when making changes elsewhere, it becomes clear the function's single responsibility is no longer needed.

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

This function does *two* things: it calculates a set of statistics about a list of numbers *and* prints them to the terminal. In violation of the rule that there should be only one reason to change a function, there are two obvious reasons this function would need to change: new or different statistics might need to be calculated or the format of the output might need to be changed. This function is better written as two separate functions: one which performs and returns the results of the calculations and another that takes those results and prints them. *One dead giveaway that 

This separation also allows for much easier testing of the function's behavior and also allows the two parts to be separated not just into two functions in the same module, but possibly live in different modules altogether if appropriate. This, too, leads to cleaner testing and easier maintenance.

Finding a function that only does *two* things is actually rare. Much more often, you'll find functions that do many, many more things.
