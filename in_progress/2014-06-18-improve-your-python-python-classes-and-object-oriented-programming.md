title: Improve Your Python: Python Classes and Object Oriented Programming
date: 2014-06-18 16:40
categories: python wip oop

The `class` is a fundamental building block in Python. It is the underpinning
for not only many popular programs and libraries, but the Python standard library as
well. Understanding what classes are, when to use them, and how the can be
useful is essential, and the goal of this article. In the process, we'll explore
what the term *Object-Oriented Programming* means and how it ties together with
Python classes.

## Everything Is An Object...

What is the `class` keyword used for, exactly? Like its function-based cousin
`def`, it concerns the *definition* of things. While `def` is used to define a
function, `class` is used to define a *class*. And what is a class? Simply a
logical grouping of data and functions (the latter of which are frequently 
referred to as "methods" when defined within a class).

What do we mean by "logical grouping"? Well, a class can contain any data we'd
like it to, and can have any functions (methods) attached to it that we please.
Rather than just throwing random things together under the name "class", we try
to create classes where there is a logical connection between things. Many
times, classes are based on objects in the real world (like `Customer` or
`Product`). Other times, classes are based on concepts in our system, 
like `HTTPRequest` or `Owner`.

Regardless, classes are a *modeling* technique; a way of thinking about
programs. When you think about and implement your system in this way, you're said to be
performing *Object-Oriented Programming*. "Classes" and "objects" are words that are 
often used interchangably, but they're not really the same thing. Understanding
what makes them different is the key to understanding what they are and how they
work.

## ..So Everything Has A Class?

Classes can be thought of a *blueprints for creating objects*. When I *define* a
Customer class using the `class` keyword, I haven't actually created a customer.
Instead, what I've created is a sort of instruction manual for constructing "customer"
objects. Let's look at the following example code:

    #!py
    class Customer(object):
        """A customer of ABC Bank with a checking account. Customers have the
        following properties:

        Attributes:
            name: A string representing the customer's name.
            balance: A float tracking the current balance of the customer's account.
        """

        def __init__(self, name, balance=0.0):
            """Return a Customer object whose name is *name* and starting
            balance is *balance*.
            self.name = name
            self.balance = balance

        def withdraw(self, amount):
            """Return the balance remaining after withdrawing *amount*
            dollars."""
            if amount > balance:
                raise RuntimeError('Amount greater than available balance.')
            self.balance -= amount
            return self.balance

        def deposit(self, amount):
            """Return the balance remaining after despositing *amount*
            dollars."""
            self.balance += amount
            return self.balance

The `class Customer(object)` line *does not* create a new customer. That is,
just because we've *defined* a `Customer` doesn't mean we've *created* one;
we've merely outlined the *blueprint* to create a `Customer` object.
To do so, we call the class's `__init__` method with the proper number of
arguments (minus `self`, which we'll get to in a moment).

So, to use the "blueprint" that we created by
defining the `class Customer` (which is used to create `Customer` objects), 
we call the class name almost as if it were a
function: `jeff = Customer('Jeff Knupp', 1000.0)`. This line simply says "use
the `Customer` blueprint to create me a new object, which I'll refer to as
`jeff`."

The `jeff` *object*, known as an *instance*, is the realized version of the `Customer`
*class*. Before we called `Customer()`, no `Customer` object existed. We can, of
course, create as many `Customer` objects as we'd like. There is still, however,
only one `Customer` *class*, regardless of how many *instances* of the class we
create.

## `self`?

So what's with that `self` parameter to all of the `Customer` methods? What is
it? Why, it's the instance, of course! Put another way, a method like `withdraw` defines the
instructions for withdrawing money from *some abstract customer's account*.
Calling `jeff.withdraw(100.0)` puts those instructions to use *on the `jeff`
instance*.

So when we say `def withdraw(self, amount):`, we're saying, "here's how you
withdraw money from a Customer object (which we'll call `self`) and a dollar
figure (which we'll call `amount`). `self` is the *instance* of the `Customer`
that `withdraw` is being called on. That's not me making analogies, either.
`jeff.withdraw(100.0)` is just shorthand for `Customer.withdraw(jeff, 100.0)`,
which is perfectly valid (if not often seen) code.

### `__init__`

`self` may make sense for other methods, but what about `__init__`? When we call
`__init__`, we're in the process of creating an object, so how can there already
be a `self`? Python allows us to extend the `self` pattern to when objects are
constructed as well, even though it doesn't *exactly* fit. Just imagine that
`jeff = Customer('Jeff Knupp', 1000.0)` is the same as calling `jeff =
Customer(jeff, 'Jeff Knupp', 1000.0)`; the `jeff` that's passed in is also
made the result.

This is why when we call `__init__`, we *initialize* objects by saying things
like `self.name = name`. Remember, since `self` *is* the instance, this is
equivalent to saying `jeff.name = name`, which is the same as `jeff.name = 'Jeff
Knupp`. Similarly, `self.balance = balance` is the same as `jeff.balance =
1000.0`. After these two lines, we consider the `Customer` object "initialized"
and ready for use.

#### Be careful what you `__init__`

After `__init__` has finished, the caller can rightly assume that the object is
ready to use. That is, after `jeff = Customer('Jeff Knupp', 1000.0)`, we can
start making `deposit` and `withdraw` calls on `jeff`; `jeff` is a
**fully-initialized** object.

Imagine for a moment we had defined the `Customer` class slightly differently:

    #!py
    class Customer(object):
        """A customer of ABC Bank with a checking account. Customers have the
        following properties:

        Attributes:
            name: A string representing the customer's name.
            balance: A float tracking the current balance of the customer's account.
        """

        def __init__(self, name):
            """Return a Customer object whose name is *name* and starting
            self.name = name

        def set_balance(self, balance=0.0):
            """Set the customer's starting balance."""
            self.balance = balance

        def withdraw(self, amount):
            """Return the balance remaining after withdrawing *amount*
            dollars."""
            if amount > balance:
                raise RuntimeError('Amount greater than available balance.')
            self.balance -= amount
            return self.balance

        def deposit(self, amount):
            """Return the balance remaining after despositing *amount*
            dollars."""
            self.balance += amount
            return self.balance

This may look like a reasonable alternative; we simply need to call `set_balance`
before we begin using the instance. There's no way, however, to communicate this
to the caller. Even if we document it extensively, we can't *force* the caller
to call `jeff.set_balance(1000.0)` before calling `jeff.withdraw(100.0)`. Since the
`jeff` instance doesn't even *have* a balance attribute until `jeff.set_balance`
is called, this means that the object hasn't been "fully" initialized.

The rule of thumb is, don't *introduce* a new attribute outside of the `__init__` method,
otherwise you've given the caller an object that isn't fully initialized. There
are exceptions, of course, but it's a good principle to keep in mind. This is
part of a larger concept of object *consistency*: there shouldn't be any series
of method calls that can result in the object entering a state that doesn't make
sense.

Invariants (like, "balance should always be a non-negative number")
should hold both when a method is entered and when it is exited. It should be
impossible for an object to get into an invalid state just by calling its
methods. It goes without saying, then, that an object should *start* in a valid
state as well, which is why it's important to initialize everything in the
`__init__` method.

## Instance Attributes

An function defined in a class is called a "method". Methods have access to all the
data contained on the instance of the object; they can access and modify
anything previously set on `self`. Because they use `self`, they require
an instance of the class in order to be used. For this reason, they're often
referred to as "instance methods".

If there are "instance methods", then surely there are other types of methods as
well, right? Yes, there are, but these methods are a bit more esoteric. 
cover them briefly here, but feel free to research these topics in more depth.

### Class Methods

*Class methods*, or *class attributes*, are attributes that are set at the
*class-level*, as opposed to the *instance-level*. Normal attributes are
introduced in the `__init__` method, but some attributes of a class hold for
*all* instances in all cases. For example, consider the following definition of
a `Car` object:

    #!py
    class Car(object):

        wheels = 4

        def __init__(self, make, model):
            self.make = make
            self.model = model

    mustang = Car('Ford', 'Mustang')
    print mustang.wheels
    # 4
    print Car.wheels
    # 4

A `Car` always has four `wheels`, regardless of the `make` or `model`. Instance
methods can access these attributes in the same way they access regular
attributes:
