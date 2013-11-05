title: Improve Your Python: Decorators Explained
date: 2013-11-05 10:49
categories: python decorators iyp

I've previously written about ["yield" and generators.](http://www.jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/) In that article, I mention it's a topic that novices find confusing. The use of **decorators** is another such topic. In this post, you'll learn what decorators are, how they're created, and why they're so useful.

<!--more-->

## A Brief Aside...

### Passing Functions

Before we get started, recall that *everything* in Python is an object that can
be treated like a value (e.g. functions, classes, modules). You can assign a
reference to these objects, pass them as arguments to functions, and return them
as the return value from functions (among other things). The following code
is an example of what I'm talking about:

    #!py
    def is_even(value):
        """Return True if *value* is even."""
        return (value % 2) == 0

    def count_occurences(target_list, predicate):
        """Return the number of times applying the callable *predicate* to a
        list element returns True."""
        return sum([1 for e in target_list if predicate(e)])

    my_predicate = is_even
    my_list = [2, 4, 6, 7, 9, 11]
    result = count_occurences(my_list, my_predicate)
    print(result)

We're writing a function that takes a list and another function, called a
*predicate* (meaning it returns True or False based on some property of the
value given to it), and returning the number of times our predicate function
holds true for the elements in the list (while there are builtin functions to
accomplish this, it's useful for illustrative purposes). 

The magic is in the lines `my_predicate = is_even`. We create a reference to the
function itself (not the value returned when calling it) and can use it like any
"normal" variable. Passing it to `count_occurences` allows `count_occurences` to
apply the function to the elements of the list, even though it doesn't "know"
what it does. It just knows it's a function that can be called with a single
argument and will return True or False.

Hopefully, this is all old news to you. If, however, this is the first time
you've seen functions used in this manner, I recommend reading [Drastically Improve Your Python: Understanding Python's Execution Model](http://www.jeffknupp.com/blog/2013/02/14/drastically-improve-your-python-understanding-pythons-execution-model/) before continuing here.

### Returning Functions

We just saw that functions can be passed as arguments into other functions. They
can also be *returned* from functions as the return value. The following
demonstrates how that might be useful:

    #!py

    def surround_with(prepend, append):
        """Return a function that takes a single argument and appends and
        prepends *value* to it."""
        def surround_with_value(word):
            return '{}{}{}'.format(prepend, word, append)
        return surround_with_value

    def transform_words(content, targets, transform):
        """Return a string based on *content* but with each occurence 
        of words in *targets* replaced with
        the result of applying *transform* to it."""
        result = ''
        for word in content.split():
            if word in targets:
                result += ' {}'.format(transform(word))
            else:
                result += ' {}'.format(word)
        print result
        return result

    my_string = 'My name is Jeff Knupp'
    transform = surround_with('<em>', '</em>')
    my_string_italicized = transform_words(my_string, ['Jeff', 'Knupp'], transform)
    print(my_string_italicized)

Here we make use of the fact that functions can be returned as the result of
calling a function to create a *new* function that, when called, prepends and
appends the given values. We then pass that new function as an argument to
`transform_words`, where it is applied to the words in our search list
(`['Jeff', 'Knupp']`).

You can think of `surround_with` as a little function factory. Its job is to
create *new* functions that, when applied to a value, surround a word with whatever 
values are supplied. Note that it doesn't actually do the surrounding itself, it 
just creates a function that can do it whenever it's needed.

`surround_with_value` makes use of the fact that nested functions have access to
references that exist in the scope in which they were created. Therefore,
`surround_with_value` doesn't need to make `prepend` and `append` parameters
(which would defeat the purpose). It simply "knows" it has access to them and 
uses them when required.

### Putting it all together
We've now seen that functions can both be sent as arguments to a function and
returned as the result of a function. What if we made use of both of those facts
together? Can we create a function that takes a function as a parameter and
returns a function as the result. Would that be useful?
