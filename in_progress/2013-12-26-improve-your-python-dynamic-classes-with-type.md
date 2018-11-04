title: Improve Your Python: Metaclasses and Dynamic Classes With Type
date: 2013-12-26 17:50
categories: python oop type metaclasses

The `type` keyword is one of those Python constructs with a well understood use
and a less widely known one. In this article, we'll explore the different, erm,
"types" of `type()`. In the process, we'll cover a good deal about Object
Oriented Programming in Python.
<!--more-->

## Are You My Type?

The first use of `type()` is the most widely known and used one: determining the
type of an object. Here, Python novices commonly interrupt and say, "But I
thought Python didn't have types!" On the contrary, *everything* in Python has a
type (even the types!) because *everything is an object*. Let's look at a few examples:

    #!py
    >>> type(1)
    <class 'int'>
    >>> type('foo')
    <class 'str'>
    >>> type(3.0)
    <class 'float'>
    >>> type(float)
    <class 'type'>

Everything is as expected, until we check the type of `float`. `<class 'type'>`?
What is that? Well, odd, but let's continue:

    #!py
    >>> class Foo(object):
    ...     pass
    ...
    >>> type(Foo)
    <class 'type'>

Ah! `<class 'type'>` again. Aparently the type of a *class itself* (not the instances of it we create) is
`type` (regarless of if they're built-in or user-defined). What about the type
of `type` itself?

    #!py
    >>> type(type)
    <class 'type'>

Well, it had to end somewhere. `type` is the type of all types, including
itself. Actually, `type` is a `metaclass`, or "a thing that builds
classes". Classes, like `list`, build instances of that class, as 
in `my_list = list()`. In the same way, `metaclasses` build types, like `list`.

Just like regular classes, `metaclasses` can be user-defined. To use it, you set
a class's `__metaclass__` attribute to the `metaclass` you built. A `metaclass`
can be any `callable`, as long as it returns a type. Usually, you'll assign a
class's `__metaclass__` to a function that, at some point, uses a variant of `type`
we've not yet discussed: `type` with three arguments creates new classes.

## The Darker Side of `type`

As mentioned, it turns out that `type` has a totally separate use, when called with three
arguments. `type(name, bases, dict)` creates a *new* type, programmatically. If
I had the following code:

    #!py
    
    class Foo(object):
        pass

I could acheive the exact same effect with the following:

    #!py
    Foo = type('Foo', (), {})

`Foo` is now referencing a class named "Foo", whose base class is `object`
(classes created with `type`, if specified without a base class, are
automatically made new-style classes).

That's all well and good, but what if we want to add member functions to Foo?
This is easily acheived by setting attributes of Foo, like so:

    #!py
    def always_false(self):
        return False

    Foo.always_false = always_false

We could have done it all in one go with the following:

    #!py
    Foo = type('Foo', (), {'always_false', always_false}

Of course, the `bases` parameter is a list of base classes of `Foo`. We've been
leaving it empty, but it's perfectly valid to create a new class derived from
`Foo`, again using `type` to create it:

    #!py
    FooBar = type('FooBar', (Foo), {})

### When Is This Ever Useful?

`type` and `metaclasses` are one of those topics that, once explained to someone, their
very next question is, "OK, so when would I use it?". The answer is, not very
often at all. However, there *are* times when creating classes dynamically with
`type` is the appropriate solution. Let's take a look at an example.

[sandman](http://www.github.com/jeffknupp/sandman) is a library I wrote to
automatically generate a REST API and web-based admin interface for existing
databases. Much of the heavy lifting is done by SQLAlchemy, an ORM framework.

There are a number of straightforward ways to register a table with SQLAlchemy.
One can describe it in a model syntax not unlink Django's. Regardless, to get
SQLAlchemy to recognize a table, a class for that table must be created.

Since `sandman` doesn't have any advanced knowledge of the database layout, it
can't rely on pre-made model classes to register tables. Rather, it needs to
introspect the database and create these classes on the fly. Sound familiar? Any
time you're creating new classes dynamically, `type` is the right/only choice.

Here's the relevant code from [sandman](https://www.github.com/jeffknupp/sandman):

    #!py
    if not current_app.endpoint_classes:
        db.metadata.reflect(bind=db.engine)
        for name in db.metadata.tables():
            cls = type(str(name), (sandman_model, db.Model),
                    {'__tablename__': name})
            register(cls)

As you can see, if the user has not manually created a model class for a table, it 
is automatically created with a `__tablename__` attribute set to the name of the
table (used by SQLAlchemy to match tables to classes).

## In Summary

In this article, we discussed the two uses of `type`, `metaclasses`, and when
the alternate use of `type` is required. Although `metaclasses` are a somewhat
confusing concept, hopefully you now have a good base off of which you can build
through further study.
