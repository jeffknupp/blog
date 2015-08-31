title: Python Dictionaries
date: 2015-08-30 17:20
categories: python datastructures

** *Aside*: one thing I dislike about the official Python documentation is that only a small percentage of entries have example code. We should change that...)**

One of the keys to becoming a better Python programmer is to have a solid grasp
of Python's built-in data structures. Using the structured format below, today you'll learn what a `dict` is, when to use it, and see example code of
*all* of its member functions. I have some other data structures in the works, so this may turn into a little series.

# Dictionary
 
## AKA
 
 "Associate Array", "Map", "Hash Map", "Unordered Map"

## Library

*built-in*

## Description

Contains a series of key -> value mappings where the "key" is of any type that is *hashable* (meaning it has both a `__eq__()` and a `__hash__()` method).  The "value" may be of any type and value types need not be homogeneous.

That means, for example, we can have a dictionary where some keys map to strings
and others to ints. Probably not a great idea in practice, but there's nothing stopping you
from doing it.

### What Makes it Special

The conceptual implementation is that of a hash table, so checks for existence are quite fast. That means we can determine if a specific `key` is present in the dictionary without needing to examine every element (which gets slower as the dictionary gets bigger). The Python interpreter can just go to the location `key` "should be" at (if it's in the dictionary) and see if `key` is actually there.

## Construction 

### Literal

* `{}`: pair of braces for empty dictionary 
* `{1:2, 3:4}`: comma-separated list of the form `key: value` enclosed by braces

    #### Constructor

* `dict(one=2, three=4)`: using `dict()` with *keyword arguments* mapping keys to values (where `one` and `two` are valid identifiers)
* `dict([(1, 2), (3, 4)])`: using `dict()` with an iterable containing iterables with exactly two objects, the key and value
* `dict(zip([1, 3], [2, 4]))`: using `dict()` with two iterables of equal length; the first contains a list of keys and the second contains their associated values.
* `dict({1:2, 3:4})`: using `dict()` with the literal form as an argument. This is silly. Why would you want this?

## Mutability

`mutable`

## Ordering

`undefined`

## When to Use It

When describing what you want to do, if you use the word "map" (or "match"), chances are good 
you need a dictionary. Use whenever a mapping from a key to a value is required. 

## Example Usage 

```
state_capitals={
    'New York': 'Albany',
    'New Jersey': 'Trenton',
    }
```

"New York" is a *key* and "Albany" is a *value*. This allows us to retrieve a state's capital if
we have the state's name by doing `capital = state_capitals[state]`

### How **Not** to Use It

*Remember, the great thing about dictionaries is we can find a value instantly,
without needing to search through the whole dictionary manually, using the form
`value = my_dict['key']` or `value = my_dict.get('key', None)`.*

**If you're searching for a value in a dictionary and you use a `for` loop,
you're doing it wrong. Stop, go back, and read the previous statement.**

All too often in beginner code I see the equivalent of the following (continuing
the previous example):

```
state_im_looking_for = 'New Jersey'
my_capital = ''

for state in state_capitals:
    if state == state_im_looking_for:
        my_capital = state_capitals[state]
```

**Or like this:**

```
state_im_looking_for = 'New Jersey'
my_capital = ''

for state, capital in state_capitals.items():
    if state == state_im_looking_for:
        my_capital = capital
```

## Methods and Uses

### `d.clear()`

Remove all entries in `d`

#### Returns

N/A

#### Raises

N/A

#### Examples

Delete all items in a dictionary

```
d.clear()
```

### `d.copy()`

Make a *shallow* copy of `d`. The dictionary returned by `d.copy()` will have
the same references as `d`, not copies of the items.

#### Returns

A new `dict`, representing a *shallow* copy of `d`

#### Raises

N/A

#### Examples

Create copy of a dictionary

```
d = {1: 'a', 2: 'b', 3: 'c'}
copied_dict = d.copy()
copied_dict # {1: 'a', 2: 'b', 3: 'c'}
d[1] = 'z'
copied_dict # {1: 'a', 2: 'b', 3: 'c'}
```

### `del k[d]`

Used to remove a value from a dictionary

#### Returns

N/A

#### Raises

`KeyError` if key is not in dictionary

#### Examples

Delete entry with key 'hello'

```
my_dictionary = {'hello': 1, 'goodbye': 2}
del my_dictionary['hello']
print(my_dictionary)
# {'goodbye': 2}
```

### `dict.fromkeys(seq[, value])`

Create a new dictionary with the same keys as `seq`. If `value` is provided,
each item's value is set to `value`. If `value` is not set, all item values are set to
`None`

#### Returns

N/A

#### Raises

N/A

#### Examples

Create a dictionary from a list with all values initialized to 0

```
my_list = [1, 2, 3]
my_dictionary = dict.fromkeys(my_list, 0)
my_dictionary # {1: 0, 2: 0, 3: 0}
```

Create a dictionary from a dictionary with all values automatically initialized to `None`

```
my_dictionary = {1: 1, 2: 2, 3: 3}
new_dictionary = dict.fromkeys(my_dictionary)
my_dictionary # {1: None, 2: None, 3: None}
```

### `d.get(key[, default)`

Used to retrieve the value associated with key `key`. The value of `default`
is returned if `key` is not in `d` (rather than raising a
`KeyError`). The default value of `default` is `None`.

#### Returns

Roughly equivalent to:

```
def get(key, default=None):
    if key in d:
        return d[k]
    else:
        return default
```

#### Raises

`KeyError` if `default` is not provided and `key` is not in `d`.

#### Examples

Get a key's value or `None` if the key isn't present
```
for key in my_dictionary:
```

### `k in d`

Used to iterate over the keys, values, or both of the dictionary.

#### Returns

N/A

#### Raises

N/A

#### Examples

Iterate over keys

```
for key in my_dictionary:
```

Iterate over `(key, value)` tuples

```
for key, value in my_dictionary.items():
```


Iterate over values

```
for value in my_dictionary.values():
```

Check for existence

```
haystack = {}
# ...
if 'needle' in haystack:
```

### `iter(d)`

Used to iterate over the keys of `d`

#### Returns

An `iterator` which iterates over the keys of `d`

#### Raises

`StopIteration` when `d` has no more keys

#### Examples

Iterate over keys

```
for key in my_dictionary:
```

### `d[key]`

Used to access the value corresponding to the key `key` in `d`.

#### Returns

Value associated with the key (heterogeneous)

#### Raises

`KeyError` when `key` is not a member of `d`.

#### Examples

```
capitals = {'New York': 'Albany'}`
capital_of_ny = capitals['New York']`
print capital_of_ny`
'Albany'
```

### `len(d)`

Used to determine the number of entries in a dictionary

#### Returns

Length of dictionary `d`

#### Raises

N/A

#### Examples

```
print 'dictionary has {} entries'.format(len(d))
```


### `k not in d`

Used for negative existence check. Equivalent to `not key in value`

#### Returns

`True` if `key` is not in `value`, `False` otherwise

#### Raises

N/A

#### Examples

Check for negative existence

```
haystack = {}
# ...
if 'needle' not in haystack:
```

### `d.keys()` 

Iterate over the keys in a dictionary

#### Returns

An iterable over all of the *keys* in `d` (in an unspecified order)

#### Raises

`StopIteration` when `d` has no more keys

#### Examples

Iterate over keys: 

```
for key in d.keys():
```

### `d.values()` 

Iterate over the values in a dictionary

#### Returns

An iterable over all of the *values* in `d` (in an unspecified order)

#### Raises

`StopIteration` when `d` has no more values

#### Examples

Iterate over values: 

```
for value in d.values():
```


### `d.items()` 

Iterate over the elements ((key, value) pairs) in a dictionary

#### Returns

An iterable over all of the (key, value) pairs in `d` (in an unspecified order).
Each (key, value) pairs is represented as a `tuple`.


#### Raises

`StopIteration` when `d` has no more elements

#### Examples

Iterate over items: 

```
for key, value in d.items():
```

Note that, in the example, we can use multiple assignment to assign `key` to the
key and `value` to the value of each item directly in the `for` loop.

### `d.pop(key[, default])`

Used to remove an item from a dictionary and return its associated value

#### Returns

`d[key]` if `key` is in `d`. If `key` is not in `d` but `default` is specified,
the `default` value is returned instead.

#### Raises

`KeyError` if `key` is not in dictionary and no `default` is specified

#### Examples

Delete entry with key 'hello' and print its value

```
my_dictionary = {'hello': 1, 'goodbye': 2}
hello_value = my_dictionary.pop('hello')
print(hello_value)
# 1
print(my_dictionary)
# {'goodbye': 2}
```

With `default` specified

```
my_dictionary = {'hello': 1, 'goodbye': 2}
foo_value = my_dictionary.pop('foo', None)
print(foo_value)
# None
print(my_dictionary)
# {'goodbye': 2}
```

With no `default` specified
```
my_dictionary = {'hello': 1, 'goodbye': 2}
foo_value = my_dictionary.pop('foo')
# KeyError: 'foo'
```


### `d.popitem()` 

Pop (i.e. delete and return) a random element from the dictionary

#### Returns

A `(key, value)` tuple if `d` is not empty.

#### Raises

`KeyError` if `d` is empty. I personally think that's a stupid exception to
raise since no key was ever specified, but, hey, I didn't write the language.

#### Examples

Destructively iterate over values:

```
try:
    key, value = d.popitem():
    print 'Got {}: {}'.format(key, value)
except KeyError:
    print 'Done'
```


### `d.setdefault(key[, default])` 

Get a `key` from the dictionary or, if it's not there, insert it with a default
value and return that. `default`, erm, defaults to `None`


#### Returns

`d[key]` if `key` is in `d`. 

If not, do `d[key] = default` and *then* return `d[key]` (which will always return `default`).

#### Raises

N/A

#### Examples

Count the number of times each word is seen in a file:

```
words = {}

for word in file:
    occurrences = words.setdefault(word, 0)
    words[word] = occurrences + 1
```


### `d.update(other)` 

Update a dictionary with the keys and values in `other`, overwriting existing
keys and values if there is any overlap.

#### Returns

`None`

#### Raises

N/A

#### Examples

Merge two dictionaries:

```
first = {'a': 1}
second = {'b': 2}
first.update(second)
print first
# {'a': 1, 'b': 2}
print second
# {'b': 2}
```

Using keyword arguments for `other`:

```
first = {'a': 1}
first.update(b=2, c=3)
print first
# {'a': 1, 'c': 3, 'b': 2}
```


