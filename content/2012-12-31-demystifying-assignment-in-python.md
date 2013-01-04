title: Demystifying Assignment in Python
date: 2012-12-31 13:12
categories: python object binding scope

When most people first hear that, in Python, "everything is an object", it triggers horrific flashbacks to languages like Java where everything the *user* writes is encapsulated in an object. Others assume this means that in the implementation of the Python interpreter, everything is implemented as objects. The first interpretation is wrong; the second is true but not particularly interesting (for our purposes). What the phrase actually refers to is the fact that all "things", be they values, classes, functions, object instances (obviously), and almost every other language construct is represented as an object. This has important implications with regards to how assignment in Python works.

A feature of the Python interpreter that confuses beginners is what happens when `print` is called on a "variable" (I'll explain the quotes in a second). Sometimes, a proper value is printed, as is the case with strings and integers. More often, though, the interpreter spits out some odd looking string like

    >> foo = Foo(bar)
    >> print(foo)
    <__main__.Foo object at 0xd3adb33f>

`print` is supposed to print the value of a "variable", right? So why is it printing that garbage?

The issue arrises from a misunderstanding about what `foo` represents in Python. Most other languages would call it a variable. Indeed, many Python articles would refer to `foo` as a variable, but as a shorthand for what `foo` actually is.

In languages like C, `foo` represents storage for "stuff". If we wrote

    int foo = 42;

it would be correct to say that the variable `foo` contained the value `42`. That is, *variables are a sort of container for values*.

In Python, there is no notion of "variables" in the C sense. When we say 

    >> foo = Foo(bar)

it would be wrong to say that `foo` contained a `Foo` object. Rather, `foo` *is a name bound to the object created by* `Foo(bar)`. The portion of the right hand side of the equals sign creates an object. Assigning `foo` to that object merely says "I want to be able to refer to this object as `foo`." **Instead of variables (in the classic sense), Python has `names` and `bindings`**.

If we continued our example and wrote

    >> baz = foo

we should read this as "Bind the name `baz` to the same object `foo` is bound to (whatever that may be)." It should be clear, then why the following happens

     >>> baz.some_attribute
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: 'Foo' object has no attribute 'some_attribute'
    >>> foo.some_attribute = 'set from foo'
    >>> baz.some_attribute
    'set from foo'
    
Changing the object in some way using `foo` will also be reflected in `baz`: they are both bound to the same underlying object. `names` can be thought of as "aliases" to objects. You can give an object as many aliases as you want; it doesn't change the underlying object at all. Changing the value using one alias will also show up in all other aliases.

Here, a questions arises: How do we know that the thing on the right hand side of the equals sign will always be an object we can bind a name to? What about

    >> foo = 10

or

    >> foo = "Hello World!"

Here's where "everything is an object" pays off. Anything you can place on the
right hand side of the equals sign is an object in Python. Both `10` and `Hello
World` are objects. Don't believe me? Check for yourself

    >> foo = 10
    >> print(f.__add__)
    <method-wrapper '__add__' of int object at 0x8502c0>

If `10` was merely a represenation of the number '10', it probably wouldn't have
an `__add__` attribute (or any attributes at all).

Since everything in Python can be though of as names and objects, we can do
stuff like this:

    >>> import datetime
    >>> datetime.datetime.now()
    datetime.datetime(2012, 12, 31, 13, 53, 59, 608842)
    >>> datetime.datetime = 'Foo'
    >>> datetime.datetime.now = 'Foo'
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: 'str' object has no attribute 'now'

Since `datetime.datetime.now` is just a name (that happens to be bound to an object representing a function), we can rebind it to whatever we please. We can even change attributes of the module itself

    >>> f = datetime
    >>> f.__name__
    'datetime'
    >>> f.__name__ = 'footime'
    >>> print(f)
    <module 'footime' from '/home/jeff/code/install/lib/python3.4/datetime.py'>

Remember, we are just changing the bindings associated with a name. What about
changing the object itself?

###Two Types of Objects

It turns out Python has two flavors of objects: `mutable` and `immutable`. 
