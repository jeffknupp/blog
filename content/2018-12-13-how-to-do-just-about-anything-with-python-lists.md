title: How To Do Just About Anything With Python Lists
date: 2018-12-13 03:02
categories: python lists

Python's `list` is one of the built-in *sequence types* (i.e. "it holds a sequence of things") is a wonderfully useful tool. I figured I'd try to determine what people are most often trying to do with lists (by analyzing Google's query data on the topic) and just bang out examples of "How do I do X with a list in Python?"

## Reverse/Sort A List In Python

There are two ways to reverse a list in Python, and which one you use depends on what you want to do with the resulting reversed data. If you're only going *iterate over* the items in the reversed list (say, to print them out), use the Python built-in function [`reversed(seq)`](https://docs.python.org/3/library/functions.html#reversed). Here's an example of `reversed` in action:

    #!py
    original_list = [1, 2, 3, 4, 5]
    for element in reversed(original_list):
        print(element)

If you need the reversed list itself, use the Python built-in function [`sorted(iterable, *, key=None, reverse=False)`](https://docs.python.org/3/library/functions.html#sorted). Let's see some examples:

    #!py
    In [10]: original_list = [3, 1, 2, 5, 4]

    In [11]: sorted(original_list)
    Out[11]: [1, 2, 3, 4, 5]

    In [15]: sorted(original_list, reverse=True)
    Out[15]: [5, 4, 3, 2, 1]

But what if your list contains more than just simple integers? How does one sort, say, a list of temperature readings over a given time if those daily readings are each stored as a  `tuples` of the form `(<date>, <daily high>, <daily low>)`? Look at the following example:

    #!py
    readings = [('1202', 45.0, 28.1), ('1201', 44.0, 33.0), ('1130', 45.0, 32.6)]

Calling `sorted(readings)` will give us a new list with the elements ordered by the `<date>` portion of the tuple (the 0-th element, since Python compares tuples lexicographically; each item is compared in order, starting with the first elements). But what if we wanted to sort by `<daily high>` or `<daily low>`? Simple! Just pass the `key` parameter a function that takes a single argument and returns the **key** for `sorted()` to use for comparisons. For example, I could sort by daily low temperatures like so:

    #!py
    In [25]: sorted(readings, key=lambda reading: reading[2])
    Out[25]: [('1202', 45.0, 28.1), ('1130', 45.0, 32.6), ('1201', 44.0, 33.0)]

In that example, we passed the `key` parameter a lambda function which accepted one argument and returned a value, in our case the third part of our temperature recording tuple (the `reading[2]` part). If we had wanted to sort by the daily high in reverse order, we would just change the call like so:

    #!py
    In [26]: sorted(readings, key=lambda reading: reading[1], reverse=True)
    Out[26]: [('1202', 45.0, 28.1), ('1130', 45.0, 32.6), ('1201', 44.0, 33.0)]

Accessing elements of a tuple or class is such a common task that Python provides a set of convenience functions in the `operator` built-in module. To access a specfic field in the tuple (as we did above for daily high as `reading[1]` and daily low as `reading[2]`), use the field's index in the tuple as an argument to `operator.itemgetter`:

    #!py
    In [29]: sorted(readings, key=itemgetter(1), reverse=True)
    Out[29]: [('1202', 45.0, 28.1), ('1130', 45.0, 32.6), ('1201', 44.0, 33.0)]

But notice that the first two entries have the same high temp recordings (`45.0`). What if we wanted to *first* sort by high temp and *then* by low temp? `itemgetter` allows for multiple levels of sorting by simply passing in multiple index values. So let's sort by high temp first, then low temp:

    #!py
    In [31]: sorted(readings, key=itemgetter(1,2), reverse=True)
    Out[31]: [('1130', 45.0, 32.6), ('1202', 45.0, 28.1), ('1201', 44.0, 33.0)]

Notice that the `('1130', 45.0, 32.6)` tuple is now first, as it had an *equal* high temp and a *greater* low temp than `('1202', 45.0, 28.1)`.

## Split A Python List Into Chunks

Splitting a list into equally sized sub-lists (for processing data in parallel, perhaps) is a common task. It's so common, in fact, that the [`itertools` module](https://docs.python.org/3/library/itertools.html) (a module practically *begging* to be used in these kinds of tasks, by the way) gives actual code for how to accomplish this in Python in the [`itertools` recpipes](https://docs.python.org/3/library/itertools.html#itertools-recipes) section of the docs. Here is the relevant code:

    #!py
    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

The code may look confusing at first, but it's simply creating `n` (or `3` in the example in the comments) separate iterators over the `iterable` argument and then cleverly zipping them back together using `zip_longest` from the `itertools` module, to collect the elements of `iterable` in a series of `n`-sized chunks.

## Flatten A Python List Of Lists Into One List

[`itertools` recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes) FTW again! Straight out of the section of the Python docs that gave us `grouper` above, the recipe for "flatten" is:

    #!py
    def flatten(list_of_lists):
        "Flatten one level of nesting."
        return chain.from_iterable(list_of_lists)

It simply calls `itertools.chain.from_iterable()` on the `list_of_lists`. A call to `flatten([[1, 2, 3], [4, 5], [6, 7, 8]])` will give us an iterator that yields each element individually. We can say `flattened_list = list(flatten([[1, 2, 3], [4, 5], [6, 7, 8]]))` if what we need is an actual list and not just an iterator.

## Insert Into A List In Python

The word "insert" here is vague (insert *where?*), but let's roll with it. Here are some of the flavors of list assignment mentioned [in the Python docs about operations on "Mutable Sequence Types"](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types):

    #!py
    Operation	Result

    s[i] = x	item i of s is replaced by x	 
    s[i:j] = t	slice of s from i to j is replaced by the contents of the iterable t	 
    s[i:j:k] = t	the elements of s[i:j:k] are replaced by those of t	(as long as t is the same length as the slice it's replacing)
    s.append(x)	appends x to the end of the sequence (same as s[len(s):len(s)] = [x])
    s.extend(t) or s += t	extends s with the contents of t (for the most part the same as s[len(s):len(s)] = t)	 
    s.insert(i, x)	inserts x into s at the index given by i (same as s[i:i] = [x])	 

So six different ways to insert into a list in Python. That doesn't seem very Pythonic!? Let's see which we might use on a case by case basis:

### Insert Into The Beginning Of A List In Python

    #!py
    s.insert(0, value)

### Insert Into The End Of A List In Python

    #!py
    s.append(value)

### Insert Into An Existing Index Of A Python List

    #!py
    s[index] = value

### Concatenating Two Python Lists

    #!py
    s += t  # Where s and t are both lists

## Python "List Index Out Of Range" Error Message

This entry is less a "how-to" and more of a "what to do when things go wrong" type of entry, but it's nonetheless searched for very often in conjuction with Python lists (for obvious reasons). The message "list index out of range" is brought to you by a specific type of built-in Exception, namely the [`IndexError`](https://docs.python.org/3/library/exceptions.html#IndexError). It is simply saying that you tried to access a list, perhaps using code like `third_value = some_list[2]`, but `2` is not a valid value because `some_list` does not have three values (we don't know how many it *does* have, just less than 3 in this case).

Want to know how many values `some_list` has? The Python built-in [`len(s)`](https://docs.python.org/3/library/functions.html#len) function will give you exactly that.

A simple debugging exercise of the "list index out of range" message might look like this:

    #!py
    def my_function(some_list):
        try:
            third_value = some_list[2]
        except IndexError:
            print(f'some_list only has {len(some_list)} entries')
            raise

Here we put our code in a `try...except` block and catch any `IndexError` exceptions that are raised. When we see one, we just print out the length of `some_list` and re-raise the exception (since we can't exactly *handle* that in any useful way). That gives me the following output:

    #!py
    In [50]: def my_function(some_list):
        ...:         try:
        ...:             third_value = some_list[2]
        ...:         except IndexError:
        ...:             print(f'some_list only has {len(some_list)} entries')
        ...:             raise
        ...:
        ...:

    In [51]: my_function([1,2])
    some_list only has 2 entries
    ---------------------------------------------------------------------------
    IndexError                                Traceback (most recent call last)
    <ipython-input-51-3f735c70ddb9> in <module>
    ----> 1 my_function([1,2])

    <ipython-input-50-137ffeaa7c70> in my_function(some_list)
        1 def my_function(some_list):
        2         try:
    ----> 3             third_value = some_list[2]
        4         except IndexError:
        5             print(f'some_list only has {len(some_list)} entries')

    IndexError: list index out of range
