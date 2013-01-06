title: Unit Testing in Django
date: 2012-02-11 14:17
categories: django python unit testing


As a follow-up to my post [Starting a Django Project the Right Way](http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/), I wanted to talk aboue the importance of writing tests for Django applications. I previously mentioned that my first site [IllestRhyme](http://www.illestrhyme.com), has no app specific tests for it. This is both embarassing and true. I've lost countless hours to fixing problems caused by new changes. I wasn't going to make the same mistake with [linkrdr](http://www.linkrdr.com). Having a set of unit tests that I can run in an automated fashion has made a world of difference.

The Django `unittest` framework (really the Python `unittest` framework) is both simple and powerfull. Along with the test client (`django.test.client.Client`), there's a lot you can
do with Django right out of the box.

Setup
---------------------------

To start, we'll want to create a dump of our database data to use during testing. 

    #!bash 
    $ ./manage.py dumpdata --format=json > my/app/directory/initial_data.json

This will give us a json [fixture](https://code.djangoproject.com/wiki/Fixtures) that mimics the current state of our production database. Note that since this is a fixture for _all_ of the apps installed, we've put it in a non-standard directory. To let the test runner find our fixture, we'll need to set `FIXTURE_DIRS` to the directory we just dumped our data to.

Now that we have our data copied, let's run whatever tests our installed
apps have already:

    #!bash
    $  python manage.py test

This hopefully gives us output like:

    #!bash
    .....................................................................................................................................................................................................................................................................................................................................................................
    ----------------------------------------------------------------------
    Ran 357 tests in 30.025s

    OK

This is also a good check of the integrity of your database, as Django
will try to load a fixture representing all of your data. If you've been
screwing around with the admin interface or the shell adding
and deleting records, you may have integrity errors. If you do (like I
did), you'll have to fix them manually and re-dump your data.

<!--more-->

Once we've got the tests for other apps working, it's time to write our
own. They'll generally all follow the same pattern:

1. Create a class deriving from django.test.TestCase
2. If necessary, add a setUp function to prepare data for the tests
3. Implement test functions with a name starting with 'test' 
4. Run the tests

You should get in the habit of running the tests after each test you
create. Sometimes, you'll write a test expecting it to pass but it will
highlight an issue in your code. If you go off and fix the issue without
running the tests again afterwards, you may have unwittingly made
another test fail with your fix. 

We'll be using `django.test.TestCase` as the base class for our tests
instead of Python's `unittest.TestCase` because the Django version adds
(from the documentation):

1. Automatic loading of fixtures
2. Wrap each test in a transaction
3. Create a TestClient instance
4. Django-specific assertions for testing for things like redirection and form errors

One quick thing to note: _all of your test functions names must begin with
'test'_. If you've never used Python or Django's unittest before, you
will be __extremely__ frustrated when you define your test classes and
functions, then run the tests only to have nothing happen. There's a
practical reason for this decision (so you can create regular functions in your
TestCase derived class), but it drives new users insane.

Adding a Test
----------------------

Time for an example. [linkrdr](http://www.linkrdr.com) needs to be able to look-up a URL and
determine if it's actually a feed. Here's a simplified version of the
code I wrote to do that:

    #!python
    link_types= ['application/atom+xml', 'application/rss+xml',
    'application/rdf+xml', 'application/xml']

    def is_feed(url):
        link_type = urllib2.urlopen(url).info().gettype()
        return link_type in link_types

Simple, right? Let's add a test for it. First we'll remove anything
hanging around in tests.py (like the initial contents) and start with a
clean file. We're going to create a class that derives from
`unittest.TestCase`. I'll call mine `IsFeed` so I know from the name
what functionality it's testing.

So far we have (with the required imports)

    #!python
    from django.utils import unittest

    class IsFeed(unittest.TestCase):

Now, we'd like to actually add some tests to our test case. Let's check
to make sure my blog's atom feed is recognized as a valid feed:


    #!python
    from django.utils import unittest

    class IsFeed(unittest.TestCase):
        """Tests the functionality of utility.is_feed
        by getting various well-known good feeds and
        making sure they validate"""

        def test_is_feed_atom(self):
        """Is the url a valid feed?"""
            url = 'http://www.jeffknupp.com/atom.xml'
            self.assertEqual(True, utility.is_feed(url))


You'll notice that I documented the test case, and you may be wondering
why, since I'm a lone developer. Two reasons. First, documentation is
just as useful for yourself as it is for others. Invariably, you'll come
back to code you wrote a while ago and decide you were drunk while you
wrote it. It just makes no sense. Having documentation helps in that
respect.

The second reason is more subtle: to prepare to open-source the project.
My goal is to eventually open-source almost all linkrdr that isn't
essential to the site. Anyone can write a function to check if a URL is
an RSS or atom feed. It would be nice to have one, though, that's been
through a lot of use and checks for odd corner-cases. To that end, I'm
attempting to keep all of linkrdr PEP8 and PEP257 compliant. It's a bit
more to write, but I'll be glad I did once I release it into the wild.

Anyway, back to our tests. We should now be able to run the tests using:

    #!bash 
    $  python manage.py test <appname>

and get output similar to when we ran the testcases before.

Code Coverage
--------------------

Tests are all well and good, but if you aren't testing a vast majority
of your code, they're just a false sense of security. Code coverage
tools are designed to intrument your test runs and determine what parts
of your tested code were actually exercised. With code coverage tools,
saying your code is 100% tested is not matter of opinion but rather a provable fact.

I use coverage.py for my code coverage. You can install it using pip via
`pip install coverage`. Once it's installed, rerun your tests like so:

    #!bash
    $  coverage run manage.py test

This will produce an instrumentation file that you can convert to HTML
or LaTex, or view from the command line. Run

    #!bash
    $  coverage report

to get a snapshot of how much of your code is actually being tested by
your unit tests.

More to Come
------------------------

I plan on continuing describing best practices for professional Django
development, started in [Starting a Django Project the Right Way](http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/) in future posts. Next time I'll discuss the TestClient and integrating tests into your deployment system.

Questions or comments on _Unit Testing in Django_? Let me know in the comments below. Also, [follow me on Twitter](http://www.twitter.com/jeffknupp) to see all of my blog posts and updates.
