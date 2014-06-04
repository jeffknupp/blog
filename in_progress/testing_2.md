In my last article, I outlined the basics of unit testing: what is is, why it's
useful, and how to do it. In this article, we'll explore the topic of testing
in more depth, covering topics like `mocking`, test suites, and test coverage,
as well as learn a bit more about third party test frameworks like
[py.test](http://pytest.org) and [nose](http://nose.readthedocs.org).

### In which I `mock` you...

It's extremely common for applications to rely on `external resources` like 
databases, network connections, and the local filesystem. **Our goal in writing unit tests is to end up with a set of tests that use no external resources.**
But if the application expects a database connection to be present, how do we
acheive this goal?

The answer is through the practice of `mocking` resources. A `mock` is
**an object we create and control that mimics an external resource in a way that is transparent to the application**. 
What does that mean? Continuing our database example, consider a simple blog application written 
using [Flask](http://flask.pocoo.org) the following code. It makes use of the 
[SQLAlchemy](http://www.sqlalchemy.org) ORM to model blog objects in the database: 

    #!py
