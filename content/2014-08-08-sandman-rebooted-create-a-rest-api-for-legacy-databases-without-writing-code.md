title: Sandman, Rebooted: Create a REST API For Legacy Databases Without Writing Code
date: 2014-08-08 14:56
categories: python sandman flask sqlalchemy

[`sandman`](http://www.github.com/jeffknupp/sandman) is by far my most popular
project. I think there's a good reason for that: it does something genuinely
useful. Ever had to deal with a legacy database through some awful system or
API? `sandman` auto-magically creates a fully RESTful API service for your
legacy database without you needing to write a line of code. You simply enter
the connection details for your database at the command line, hit enter, and
"hello REST API!".

That's all great, but what about the code that powers it? I'll be the first to
admit that `sandman`, while well-tested and well-documented, is implemented in a
bit of a crazy way. The reason for this is a combination of my limited knowledge
(at the time) of SQLAlchemy and a few shortcomings in SQLAlchemy's reflection
capabilities. I had to do some code gymnastics to get it all working properly.

But SQLAlchemy released a new major version (0.9) with a new, if
under-publicized, feature called "automapping". This is as perfect a fit for
`sandman` as it sounds: you can use it to automatically create classes based on
reflected database tables. Once I saw this, I instantly realized this could be a
boon to simplifying `sandman`. Still, though, I hadn't been writing REST APIs
for very long and didn't have a great handle on how to generalize things enough
to properly make use of `automap`.

That changed in the past few months, though, and in the back of my mind I began
to hear the siren's song calling me to rewrite `sandman` from scratch. The
problem, though, was the original `sandman` worked. It worked due to awesome
people entering Issues on GitHub and me feeling bad that *my baby* had problems
(my `sandman` baby. Not Alex, my real baby, who is perfect). I didn't want to 
lose all the work I had put into `sandman`.

Finally, yesterday, I decided to pull the trigger and see just how small I could
make `sandman`. As it seems to be the most used feature, I decided to focus just
on the case where the user wants `sandman` to reflect all of their database
tables and doesn't want to customize anything. How quickly, and in how many
lines of code, could it be done?

# Very Quickly, and Not Many

It turns out that it took about an hour to get a working REST API that I could
`curl` to my heart's content. Like the original `sandman`, give it a database
URI and it automatically creates a RESTful API service (though this one doesn't
include the admin interface, since it's not part of the core offering and it 
would be trivial to add this later).

It took about 300 lines of code (I'm not counting the `exception.py` file, which
is just boilerplate error handling). If you're interested, you can [check it out here](http://www.github.com/jeffknupp/sprime).
You'll notice there's no `setup.py`, no tests, no documentation. You simply
install `Flask-SQLAlchemy`, run `runserver.py`, and starting `curl`-ing
`localhost:5000`. Here are a few of the available endpoints in the 
example database:

* artist
* track
* genre
* playlist
* album

You can get all the tracks, for example, by doing `$ curl http://localhost:5000/track`.
All the normal HTTP methods work as expected.

# How?

The key insight I had was that you can actually create a REST endpoint for an
ORM model without knowing anything about it, aside from a few things that
SQLAlchemy guarantees. Imagine we define the
following class:

    #!python
    class Service(object):

        __model__ = None

        # def get(...):
        # 
        # def post(...):
        #
        # def put(...):
        # 
        # ...
        
We will set `__model__` to the ORM model class during application start up. To handle a POST,
we know we need to create a new instance of the `__model__` class. We know we can at
least say:

    #!python
    def post(self):
        new_instance = self.__model__()

and create a new *empty* instance. But that's not what we want. Presumably, a
bunch of JSON was sent in on the request with the initial values for the
instance. How, without knowing each individual field required for this specific
class, can we create an instance with the proper values?

Quite simply, it turns out. We can do something I can only describe as "cute"
using two facts: SQLAlchemy model classes provide a version of `__init__`
with each field as a keyword argument, and a dictionary can be transformed into
a series of keyword arguments in a function call using `**`. Since our JSON is
represented on the server as a dictionary of fields and their values, we can
simply say:

    #!python
    def post(self):
        new_instance = self.__model__(**request.json)

We've cleverly combined the two facts above to initialize an object with specific
values *without knowing the names of the attributes on the object*. That's kind
of nifty.

# Another Trick

The other part that's a bit tricky is the registration of routes. We know, for a
table named, say, `artist`, we can register `/artist` with the `GET` and `POST`
methods. But wait! We also need to handle `/artist/<id>`, which can be called
via `GET` to get a specific resource. It seems that we need two different `get`
methods: one that takes no parameters and another that takes an `id`.

There's a simple way around this, and that's to create a single `get` method
with `id` as an optional parameter defaulting to `None`. We then *register the `get` method twice*: once
with the `id` parameter and once without. I didn't actually realize that was
allowed until I saw it in a code sample sometime last year. Anyway, the full
route registration code looks like this:

    #!python
    def register_endpoint(cls, app, primary_key='resource_id', primary_key_type='int')
        view_func = cls.as_view(cls.__endpoint__)
        app.add_url_rule(
            cls.__url__, defaults={primary_key: None},
            view_func=view_func,
            methods=['GET'])
        app.add_url_rule(cls.__url__, view_func=view_func, methods=['POST', ])
        app.add_url_rule(
            '{resource}/<{pk_type}:{pk}>'.format(
                resource=cls.__url__, pk=primary_key, pk_type=primary_key_type),
            view_func=view_func,
            methods=['GET', 'PUT', 'PATCH', 'DELETE'])

# Summing Up

And that's basically it. I took the file `service.py` from a project I'd written
earlier and `model.py` straight from `sandman`. I added a bit of glue code, and
that was that. A complete REST API, including things like pagination, for *any* legacy
database in **only 300 lines of code.** I don't know about you, but I'm pretty
impressed at the power of all the tools involved.

I'm not sure if I'll continue working on the [sprime](http://www.github.com/jeffknupp/sprime)
repository. Like I said, there's a lot that's missing from it that would need to
be transferred from `sandman`. It *is*, however, a much cleaner design, and
lends itself nicely to extension. So there's a greater than zero chance that
what you're looking at is really a preview of the new `sandman`. If I continue
on the sprime repo, there are some *really* cool things I can do as a result of
the new design, but I'll leave them as an exercise for the reader/topic of
another blog post :)
