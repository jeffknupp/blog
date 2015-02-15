title: Improve Your Python: Learn Python's Data Structures
date: 2014-10-05 17:16
categories: python iyp datastructures

One of the keys to becoming a veteran programmer (in any langauge) is to become
intimately familiar with data structures; most importantly, when to use each
one. Part of Python's popularity is based on the strength of its data
structures. You can get a long way just using lists, dicts, and sets.
In this article, we'll review core Python data structures, explain what
they are and how they're used, and see why each one should have a place in your
toolbelt.

First, let's briefly review the data structures. We'll consider only the most general
ones: the built-in data types and the members of the `collections` class.

## Python Data Structures

* Dictionary
* List
* Tuple
* Set
* Frozenset
* Named Tuple
* Deque
* Counter
* Ordered Dict
* Default Dict

For each, we'll identify a number traits like *ordering* and *mutability*.
*Ordering* describes whether or not iterating over the structure is supported
and, if so, if the order is defined. *Mutability* describes if a structure is
"changeable". Strings, for example, are *immutable* in Python, meaning that once
you create a string, you can't change it. You can only modify a string by
creating a new one. Lists, on the other hand, are *mutable*. Even after it is
initially created, you can add elements to a list, thus changing it.

Let's take a look at each one in more detail:

### Dictionary

##### AKA

* Associate Array
* Map
* Hash Map
* Unordered Map

##### Library

`built-in`

##### Description

Contains a series of key->value mappings where the "key" is of any type
that is *hashable*, meaning it has both a `__eq__()` and a `__hash__()` method.
The "value" may be of any type and value types need not be homogenous

##### What Makes it Special

The underlying implementation is that of a hash table, so checks for existence are quite fast. 

##### Construction 
    
* `{}`: pair of braces for empty dictionary 
* `{1:2, 3:4}`: comma-separated list of the form `key: value` enclosed by braces
* `dict(one=2, three=4)`: using `dict()` with *keyword arguments* mapping keys to values
    (where `one` and `two` are valid identifiers)
* `dict([(1, 2), (3, 4)])`: using `dict()` with an iterable containing
    iterables with exactly two objects, the key and value
* `dict(zip([1, 3], [2, 4]))`: using `dict()` with two iterables of
    equal length; the first contains a list of keys and the second
    contains their associated values.
* `dict({1:2, 3:4})`: using `dict()` with the literal form as an
    argument. This is silly. Why would you want this?

##### Mutability

`mutable`

##### Ordering

`undefined`

##### When to Use It

When describing what you want to do, if you use the word "map" (or "match"),
chances are good you need a dictionary. Use whenver a mapping from a key to a value is required. 

##### Example Usage

    #!py
    state_captials={'New York': 'Albany'}

"New York" is a *key* and "Albany" is a *value*. This allows us to retrieve a state's
captial if we have the state's name by doing `captial = state_captials[state]`

----------------------------------------------------------------

### List

##### AKA

* Array
* Vector

##### Library

`built-in`

##### Description

Contains a series of (possibly) heterogeneous values

##### What Makes it Special

A work-horse data structure, the `list` is notable for its overall
utility. It provides storage for a mutable sequence of values and
iteration order is well-defined. Appending to the end of a `list`
is an extremely fast operation. Removing or inserting from the middle
is a good deal slower.

##### Construction

* `[]`: pair of empty square-brackets for empty list
* `[1, 2, 3]`: comma-separated list containing initial values
* `[element for element in interable]`: as list comprehension over
    existing iterable
* `list()`: using `list()` to create an empty list
* `list(iterable)`: using `list()` with an iterable to be used as the initial
    series of values 

##### Mutability

`mutable`

##### Ordering

`defined: insertion order`

##### When to Use It

Whenever a list of values is needed, especially if the ordering of values is important.

##### Example Usage

    #!py
    stooges = ['Larry', 'Moe', 'Curly']

Each element can be retrieved using its zero-based index in the list (i.e. "Moe" is index `1`). 

-------------------------------------------------------

### Set

##### AKA

* Hash Set 
* Unordered Set

##### Library

built-in

##### Description

Contains a *hashable* series of distinct elements. Attempts to insert a duplicate element are ignored.

##### What Makes it Special

Each element is hashed as it is added, making *existence checks* quite fast.
This also prevents multiple copies of the same element from being added.

##### Construction

* `set(iterable)`: using `set()` to create a set comprised of the
    elements of `iterable`. Duplicate elements contained in `sequence` are
    silently removed.
* `{1, 2}`: comma-separated list of initital values surrounded by braces
     
##### Mutability

`mutable`

##### Ordering

`undefined`

##### When to Use It

When you want to remove duplicates from an existing sequence, or when you need
to perform numerous existence checks on a sequence. Also, sets support the
mathematical set operations like *union*, *difference*, etc.

##### Example Usage

    #!py
    def get_unique_elements(values):
        uniques = set()
        for name in values:
            uniques.add(name)
        return uniques

    print(get_unique_elements([1, 2, 3, 2, 3, 1, 4, 5]))
    >> {1, 2, 3, 4, 5}

Notice calls to `add` for elements already present in the set are a no-op

----------------------------------------------------------------

### Frozenset

##### AKA

* Immutable Set

##### Library

`built-in`

##### Description

Contains a series of non-duplicated elements. Attempts to insert a duplicate element are ignored

##### What Makes it Special

Like the `set` element is hashed as it is added, making *existence checks* quite fast.
`frozenset`s, however, are *immutable* (hence the "frozen" prefix).

##### Construction

* `frozenset(iterable)`: using `frozenset()` to create a set comprised of the
    elements of `iterable`. Duplicate elements contained in `sequence` are silently removed.

##### Mutability

`immutable`

##### Ordering

`undefined`

##### When to Use It

Think of it as `list:tuple :: set:frozenset`. The former examples are `mutable`,
the latter are `immutable`. *Immutability* is a desirable property (when
appropriate) for a data structure as it allows for efficient storage and
searching.

Also, a `list` or `tuple` element need not be hashable. Since existence checks
are not guaranteed to be `O(1)`, *anything* can be used as a value. A `set` or
`frozenset` element must be hashable, to allow for efficient lookup.

##### Example Usage

    #!py
    VALID_ASCII_VALUES = frozenset(range(128))

    def is_legal_ascii_value(value):
        return value in VALID_ASCII_VALUES
        
The list of valid ASCII values is not going to change. At the same time, we are
going to be doing frequent existence checks, so having the hashability guarantee
of a `frozenset` is attractive.

-------------------------------------------------------

### Tuple

##### AKA

* N-Tuple

##### Library

built-in

##### Description

An immutable sequence of values with a defined iteration order

##### What Makes it Special

The `tuple` is behind a number of common Python idioms including multiple assignment
and returning multiple values from a function.

##### Construction
 
* `element, element`: comma separated list of elements with or without
    enclosing parenthesis. Note the comma is the operator in this case
    (not the parentheses)
* `tuple(iterable)`: using `tuple()` to construct a tuple from an
    iterable

##### Mutability

`immutable`

##### Ordering

`defined: insertion order`

##### When to Use It

Use a tuple where you might otherwise use a list, but you know that the elements won't need to change. 

##### Example Usage

If you have a program that checks if a string is a supported HTTP method, you might define them as a tuple: 

    #!py
    SUPPORTED_HTTP_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

The list of supported methods isn't going to change over the life of the program,
so it's more appropriate to use a `tuple` here than, say, a `list`.
