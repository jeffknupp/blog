title: Flask and SQLAlchemy Magic
date: 2015-07-12 11:45
categories: python flask sqlalchemy

For my first "real" post after my extended leave, I wanted to cover something fun (well, fun if you like writing libraries with Flask and SQLAlchemy...). In one of my projects at work recently, I was tasked with turning a client-facing Flask app that I had written into a framework/library that made creating new "sub-applications" as easy as possible. One pattern that had worked well in the original app was the use of Flask-SQLAlchemy, both for interacting with a new set of database models and in connecting to existing databases owned by other teams. One existing database, in particular, was heavily used by the app and would likely be used a good deal by any "sub-apps" created on the framework.

The database in question was essentially our company's "main" database, with
about 100 tables (each with thousands or millions of records). This is a common, and somewhat frustrating situation when writing internal libraries: you know clients are going to need to use some resource, but you're not exactly sure how or what parts of it. How do you create an interface to that? With SQLAlchemy specifically, does that mean each sub-project will need to describe all of the tables it needs to use from the "main" database, leading to repeated, boilerplate code? Of course not! All it takes is a little *magic*.

<!--more-->

To understand the problem a bit better, pretend that the "main" database is a
database of songs, artists, tracks, albums, and genres (with the appropriate
foreign-key relationships between each table). The original application may only
need songs and artists. Sub-app `Foo` may only need artists and albums. Sub-app
`Bar` may only need access to songs.

We want to provide access to these tables as Flask-SQLAlchemy models, *but only the ones required by the
sub-app*. That is, we don't want to use reflection on *all* of the tables in the
database. And of course, we want these tables to be available dynamically. That
is, there shouldn't need to be any code that tells the library ahead of time
what tables will be required.

## SQLAlchemy and `automap`

Sounds like a tough challenge, right? SQLAlchemy is perfectly capable of
reflecting the entire database, and we might be able to use that to create
Flask-SQLAlchemy db models on the fly, but how do we get only what the client
wants? And what would the interface to this be? We don't want something big and
clunky, like requiring the client to call a function each time it wants to
access a new model class.

In fact, ideally, library users would be able to say `from
framework.models.main_database import Artist, Album` and we would take care of
the import using some SQLAlchemy, erm, alchemy. It turns out, this is not just possible, it's
actually rather easy. I'll post the code below; study it for a few minutes and try to determine
how it works.

```
MAIN_DATABASE_MODEL_MAP = {
    'artist_table': 'Artist',
    'album_table': 'Album',
}

# The `framework.models.main_database` module`...

def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    name = referred_cls.__name__.lower()
    local_table = local_cls.__table__
    if name in local_table.columns:
        newname = name + "_"
        return newname
    return name

def name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    name = referred_cls.__name__.lower() + '_collection'
    for c in referred_cls.__table__.columns:
        if c == name:
            name += "_"
    return name

with app.app_context():
    engine = create_engine(app.config['MAIN_DATABASE_URI'])
    metadata = MetaData(engine)
    session = Session(engine)
    metadata.reflect(bind=engine, only=app.config['MAIN_DATABASE_MODEL_MAP'].keys())
    Model = declarative_base(metadata=metadata, cls=(db.Model,), bind=engine)
    Base = automap_base(metadata=metadata, declarative_base=Model)
    Base.prepare(
        name_for_scalar_relationship=name_for_scalar_relationship,
        name_for_collection_relationship=name_for_collection_relationship
        )

    for cls in Base.classes:
        cls.__table__.info = {'bind_key': 'main'}
        if cls.__table__.name in app.config['MAIN_DATABASE_MODEL_MAP']:
            globals()[app.config['MAIN_DATABASE_MODEL_MAP'][cls.__table__.name]] = cls
```

*Note: `MAIN_DATABASE_MODEL_MAP` is used purely for the user's convenience, allowing them to name the Flask-SQLAlchemy class that will be created for a given table something other than the table's name. It's not strictly necessary.*

## What Just Happened?

Like I said, this code was really "for fun" and not hugely useful to 99% of projects, but it's neat regardless. We use SQLAlchemy's new `automap_base` functionality, along with SQLAlchemy `MetaData` objects' ability to reflect only an enumerated list of tables in the database. Between them, we insert a `declarative_base` that derives from Flask-SQLAlchemy's `db.Model` class. Once that's created, we call `prepare` on `Base` (remember, returned by `automap_base` rather than the more common `declarative_base`). 

Then, for each class that is mapped by `Base`, we inject the given `cls` (with the desired class name defined by the user in `MAIN_DATABASE_MODEL_MAP`) into the module's global scope using the dictionary returned by `globals()`. This dictionary represents all names that the module should make available at the global scope. That now includes our dynamically generated, Flask-SQLAlchemy model classes as well, letting the user say `from framework.models.main_database import Artist, Album`, exactly as desired!

## OK, But... Really?

Though it's a bit of fun, if you don't immediately understand what the code is
doing (or how), study it a bit, line by line, until it becomes clear. Using the
interactive interpreter (or, better, IPython) can be helpful here.

Hope you enjoyed this quick article. Hopefully, there will be more coming soon :)
