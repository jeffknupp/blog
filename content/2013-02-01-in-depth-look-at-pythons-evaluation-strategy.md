title: Demystifying Assignment in Python
date: 2012-12-31 13:12
categories: python object binding scope

Those new to Python are often surprised by the behavior of their own code. They
expect *A* but, seemingly for no reason, *B* happens instead.
The root cause of many of these "surprises" is confusion about the Python
data model. It's the sort of thing that, if it's explained to you once, a number of
Python concepts that seemed hazy before become crystal clear. It's also really
difficult to just "figure out" on your own, as it requires a fundamental shift
in thinking about core language concepts like variables, objects, and functions.

In this post, I'll help you understand what's happening behind the scenes when
you do common things like creating a variable or calling a function. As a
result, you'll write cleaner, more comprehensible code. You'll also become a
better (and faster) reader of code. All that's necessary is to forget everything
you know about programming.


When most people first hear that, in Python, "everything is an object", it triggers 
flashbacks to languages like Java where everything the *user* writes is encapsulated 
in an object. Others assume this means that in the implementation of the Python 
interpreter, everything is implemented as objects. The first interpretation is 
wrong; the second is true but not particularly interesting (for our purposes). 
What the phrase actually refers to is the fact that all "things", be they values, 
classes, functions, object instances (obviously), and almost every other language 
construct is conceptually an object. 

What does it mean for everything to be an object? It means all of the "things" 
mentioned above have all the properties we usually associate with 
objects (in the object oriented sense); types have member functions, functions 
have attributes, modules can be passed as arguments, etc. This has important 
implications with regards to how assignment in Python works.

A feature of the Python interpreter that confuses beginners is what happens 
when `print` is called on a "variable" (I'll explain the quotes in a second). 
Sometimes, a proper value is printed. This is the case with strings and integers. 
More often, though, the interpreter spits out some odd looking string like

    #!py
    >> class Foo: pass
    >> foo = Foo(bar)
    >> print(foo)
    <__main__.Foo object at 0xd3adb33f>

`print` is supposed to print the value of a "variable", right? So why is it 
printing that garbage?

To answer that, we need to understand what `foo` actually represents in Python. 
Most other languages would call it a variable. Indeed, many Python articles 
would refer to `foo` as a variable, but as a shorthand for what `foo` actually 
is.

In languages like C, `foo` represents storage for "stuff". If we wrote

    #!c
    int foo = 42;

it would be correct to say that the integer variable `foo` contained the 
value `42`.  That is, *variables are a sort of container for values*.

In Python, this isn't the case. When we say:

    #!py
    >> foo = Foo(bar)

it would be wrong to say that `foo` contained a `Foo` object. 
Rather, `foo` *is a name bound to the object created by* `Foo(bar)`. 
The portion of the right hand side of the equals sign creates an object. 
Assigning `foo` to that object merely says "I want to be able to refer 
to this object as `foo`." **Instead of variables (in the classic 
sense), Python has `names` and `bindings`**.

So when we printed `foo` earlier, what the interpreter was showing us was the
address in memory of the object `foo` is bound to. This isn't as useless as it
sounds. If you're in the interpreter and want to see if two names are bound to
the same object, you can check by printing them and comparing the addresses. If
they match, it's the same object; if not, their bound to different objects. Of
course, the idiomatic way to check if two names are bound to the same object is
to use `is` (more on that in a bit).

If we continued our example and wrote

    #!py
    >> baz = foo

we should read this as "Bind the name `baz` to the same object `foo` is bound 
to (whatever that may be)." It should be clear, then why the following happens

    #!py
     >>> baz.some_attribute
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: 'Foo' object has no attribute 'some_attribute'
    >>> foo.some_attribute = 'set from foo'
    >>> baz.some_attribute
    'set from foo'
    
Changing the object in some way using `foo` will also be reflected in `baz`: they 
are both bound to the same underlying object. `names` in Python are not unlike names 
in the real world. If my wife calls me "Jeff", my dad calls me "Jeffrey", and my 
boss calls me "Idiot", it doesn't fundamentally change *me*. If my boss decides 
to call me "Captain Programming," great, but it still hasn't changed anything 
about me. It does mean, however, if my wife kills "Jeff", "Captain Programmer" is 
also dead. Likewise, in Python binding a name to an object doesn't change it. Changing 
some property of the object, however, will be reflected in all other names bound 
to that object.

Here, a questions arises: How do we know that the thing on the right hand side of 
the equals sign will always be an object we can bind a name to? What about

    #!py
    >> foo = 10

or

    #!py
    >> foo = "Hello World!"

Here's where "everything is an object" pays off. Anything you can (legally) place 
on the right hand side of the equals sign is an object in Python. Both `10` 
and `Hello World` are objects. Don't believe me? Check for yourself

    #!py
    >> foo = 10
    >> print(foo.__add__)
    <method-wrapper '__add__' of int object at 0x8502c0>

If `10` was actually just the number '10', it probably wouldn't have
an `__add__` attribute (or any attributes at all).

To see what attributes `10` has, we use the `dir()` function:

    #!py
    >>> dir(10)
    ['__abs__', '__add__', '__and__', '__class__', '__cmp__', '__coerce__', '__delattr__', 
    '__div__', '__divmod__', '__doc__', '__float__', '__floordiv__', '__format__', 
    '__getattribute__', '__getnewargs__', '__hash__', '__hex__', '__index__', 
    '__init__', '__int__', '__invert__', '__long__', '__lshift__', '__mod__', 
    '__mul__', '__neg__', '__new__', '__nonzero__', '__oct__', '__or__', 
    '__pos__', '__pow__', '__radd__', '__rand__', '__rdiv__', '__rdivmod__', 
    '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', 
    '__rmod__', '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', 
    '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', 
    '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 
    'bit_length', 'conjugate', 'denominator', 'imag', 'numerator', 'real']

With all those attributes and member functions, I think it's safe to say `10` is
an object.

Since everything in Python is just names and objects, we can do
stuff like this:

    #!py
    >>> import datetime
    >>> datetime.datetime.now()
    datetime.datetime(2012, 12, 31, 13, 53, 59, 608842)
    >>> datetime.datetime = 'Foo'
    >>> datetime.datetime.now() 
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: 'str' object has no attribute 'now'

`datetime.datetime.now` is just a name (that happens to be bound to an object 
representing a function that calculates the current date and time). We can rebind it 
to whatever we please. We can even change attributes of the module itself

    #!py
    >>> f = datetime
    >>> f.__name__
    'datetime'
    >>> f.__name__ = 'footime'
    >>> print(f)
    <module 'footime' from '/home/jeff/code/install/lib/python3.4/datetime.py'>

At this point, we've only changed bindings associated with a name. What about
changing the object itself?

###Two Types of Objects

It turns out Python has two flavors of objects: `mutable` and `immutable`.
The value of mutable objects can be changed after they are created. The value of
immutable objects cannot. A `list` is a mutable object. You can create a list,
append some values, and the list is updated in place. A `string` is immutable.
Once you create a string, you can't change its value. 

I know what you're thinking. "Of course you can change the value of a string, I
do it all the time in my code!" When you "change" a string, you're actually
rebinding it to a newly created string object. The original object remains
unchanged, even though its possible that nothing refers to it anymore.

See for yourself:

    #!py
    >>> a = 'foo'
    >>> a
    'foo'
    >>> b = a
    >>> a += 'bar'
    >>> a
    'foobar'
    >>> b
    'foo'

Even though we're using `+=` and it *seems* that we're changing the string, we
just get a new one containing the result of the change. This is why you may hear
people say, "string concatenation is slow.". It's because concatenating strings
must allocate memory for a new string and copy the contents, while appending to
a list (in most cases) requires no allocation. Immutable objects are
fundamentally expensive to "change", because doing so involves creating a copy.
Changing mutable objects is cheap.

###Immutable object weirdness

When I said the value of immutable objects can't change after their created, it
wasn't the whole truth. A number of containers in Python, like `set` are immutable.
The value of a `set` can't be changed after it is created. But the "value" of a
set is conceptually just a list of unchangeable names bound to some objects. 
The key thing to note is that the *bindings* are unchangeable, not the objects 
they are bound to.

This means the following is perfectly legal:
    
    #!py
    >>> class Foo():
    ...     def __init__(self):
    ...             self.value = 0
    ...     def __str__(self):
    ...             return str(self.value)
    ...     def __repr__(self):
    ...             return str(self.value)
    ... 
    >>> f = Foo()
    >>> print(f)
    0
    >>> foo_tuple = (f, f)
    >>> print(foo_tuple)
    (0, 0)
    >>> foo_tuple[0] = 100
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError: 'tuple' object does not support item assignment
    >>> f.value = 999
    >>> print(f)
    999
    >>> print(foo_tuple)
    (999, 999)

This is a subtle point, but nonetheless important: the "value" of an immutable
object *can't* change, but it's constituent objects *can*. 

###Function calls

If variables are just `names` bound to objects, what happens when we pass them
as arguments to a function? The truth is, we don't really pass all that much.
Take a look at this code:

    #!py
    def add_to_tree(root, value_string):
        """Given a string of characters `value_string`, create or update a
        series of dictionaries where the value at each level is a dictionary of
        the characters that have been seen following the current character.

        Example:
        >>> my_string = 'abc'
        >>> tree = {}
        >>> add_to_tree(tree, my_string)
        >>> print(tree['a']['b'])
        {'c': {}}
        >>> add_to_tree(tree, 'abd')
        >>> print(tree['a']['b'])
        {'c': {}, 'd': {}} 
        >>> print(tree['a']['d'])
        KeyError 'd'
        """

        for character in value_string:
            root = root.setdefault(character, {})


We're essentially creating an autovivifying dictionary that operates like a
trie. Notice that we change the `root` parameter in the `for` loop. And yet
after the function call completes, `tree` is still the same dictionary with some
updates. It is *not* the last value of `root` in the function call. So in one
sense `tree` is being updated; in another sense it's not.

To make sense of this, consider what the `root` parameter actually is: a *new* binding
to the object reffered to by the name `root`. In the case of our example, `root`
is a name bound to the same object as `tree`. It is *not* `tree` itself, which
explains why changing `root` in the function leaves `tree` unchanged. As you'll
recall, assinging `root` to `root.setdefault(character, {})` merely rebinds
`root` to the object created by the `root.setdefault(character, {})` statement.

Here's an even more straightforward example:

    #!py
    def list_changer(input_list):
        input_list[0] = 10

        input_list = range(1, 10)
        print(input_list)
        input_list[0] = 10
        print(input_list)

    >>> test_list = [5, 5, 5]
    >>> list_changer(test_list)
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    [10, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> print test_list
    [10, 5, 5]

Our first statement *does* change the value of the underlying list (as we can
see in the last line printed). However, once we rebind the name `input_list` by
saying `input_list = range(1, 10)`, **we're now referring to a completely
different object**. We basically said "bind the name `input_list` to this new list." 
After that line, we have no way of referring to the original `input_list` parameter 
again. 

By now, you should have a clear understanding of how binding a name works.
There's just one more item to take care of.

###Blocks and Scope
