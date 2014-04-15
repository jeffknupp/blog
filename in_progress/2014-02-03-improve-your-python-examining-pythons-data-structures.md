title: Improve Your Python: Examining Python's Data Structures
date: 2014-02-03 10:34
categories: python improveyourpython

My tutoring clients often ask if they should be creating classes for the simple
data structures in their programs. I almost always reply, "No," as Python's built-in
data structures (i.e. lists, dictionaries, sets, tuples) are quite powerful and
are normally up to the task. In this article, we'll dive into Python's data
structures in order to understand what they are, when to use them, and how to do
so.

## Data Structure Directory

First things first: let's take stock of the data structures built-in to the
language. In the list below, I've listed the name of the data structure and the
type of data it contains. Later we'll see how they work and when to use them.

* Dictionary
    * AKA: "Associate Array", "Map", "Hash Map", "Unordered Map"
    * Library: built-in
    * Description: Contains a series of key->value mappings where the "key" is of any type
      that is *hashable* (meaning it has both a `__eq__()` and a `__hash__()` method).
      The "value" may be of any type and value types need not be homogenous
    * What Makes it Special: The underlying implementation is that of a hash
      table, so checks for existence are quite fast. 
    * Construction 
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
    * Mutability: `mutable`
    * Ordering: `undefined`
    * When to Use It: When describing what you want to do, if you use the word
      "map" (or "match"), chances are good you need a dictionary. Use whenver a
      mapping from a key to a value is required. 
    * Example Usage: `state_captials={'New York': 'Albany'}` "New York" is a *key*
      and "Albany" is a *value*. This allows us to retrieve a state's captial if
      we have the state's name by doing `captial = state_captials[state]`
* List
    * AKA: "Array", "Vector"
    * Library: built-in
    * Description: Contains a series of (possibly) heterogeneous values
    * What Makes it Special: A work-horse data structure, the `list` is notable
      for its overall utility. It provides storage for a mutable sequence of
      values and iteration order is well-defined. Appending to the end of a
      `list` is an extremely fast operation. Removing or inserting from the
      middle is a good deal slower.
    * Construction
        * `[]`: pair of empty square-brackets for empty list
        * `[1, 2, 3]`: comma-separated list containing initial values
        * `[element for element in interable]`: as list comprehension over
          existing iterable
        * `list()`: using `list()` to create an empty list
        * `list(iterable)`: using `list()` with an iterable to be used as the initial
          series of values 
    * Mutability: `mutable`
    * Ordering: `defined`
    * When to Use It: Whenever a list of values is needed, especially if the ordering 
      of values is important.
    * Example Usage: `stooges = ['Larry', 'Moe', 'Curly']` Each element can be
      retrieved using its zero-based index in the list (i.e. "Moe" is index `1`). 
* Set
    * AKA: "Hash Set", "Unordered Set"
    * Library: built-in
    * Description: Contains a series of non-duplicated elements. Attempts to insert a duplicate element are ignored
    * What Makes it Special: Each element is hashed as it is added, making *existence checks* 
      quite fast. This also prevents multiple copies of the same element from
      being added.
    * Construction
        * `set(iterable)`: using `set()` to create a set comprised of the
          elements of `iterable`. Duplicate elements contained in `sequence` are
          silently removed.
        * `{1, 2}`: comma-separated list of initital values surrounded by braces
    * Mutability: `mutable`
    * Ordering: `undefined`
* Tuple
    * AKA: "N-Tuple"
    * Library: built-in
    * Description: An immutable sequence of values with a defined iteration order
    * What Makes it Special: The `tuple` is behind a number of common Python
    idioms including multiple assignment and returning multiple values from a
    function.
    * Construction
        * `element, element`: comma separated list of elements with or without
          enclosing parenthesis. Note the comma is the operator in this case
          (not the parentheses)
        * `tuple(iterable)`: using `tuple()` to construct a tuple from an
          iterable
    * Mutability: `immutable`
 * Frozenset
    * AKA: "Immutable Set"
    * Library: built-in
    * Description: Contains a series of non-duplicated elements. Attempts to insert a duplicate element are ignored
    * What Makes it Special: Like the `set` element is hashed as it is added, making *existence checks* 
      quite fast. `frozenset`s, however, are *immutable* (hence the "frozen" prefix).
    * Construction
        * `frozenset(iterable)`: using `frozenset()` to create a set comprised of the
          elements of `iterable`. Duplicate elements contained in `sequence` are
          silently removed.
    * Mutability: `immutable`
    * Ordering: `undefined`
* Queue
