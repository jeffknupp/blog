title: Flask and SQLAlchemy Architectual Patterns
date: 2014-06-04 13:08
categories: python flask sqlalchemy

After spending some time developing applications with [Flask](http://flask.pocoo.org) and [SQLAlchemy](http://www.sqlalchemy.org)
(and [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)), I've
noticed certain patterns when it comes to the system architecture. What follows
below is sort of a hodge-podge jumble of stuff I've come to learn after spending
time developing with Flask and SQLAlchemy.

## Project Layout

Imagine we run an online music service and want to create a REST API 
for internal use. If we call our application `music`, here's the directory
layout I tend to use:

    $ tree
    .
    ├── models.py
    ├── music
    │   ├── __init__.py
    │   └── models.py
    └── runserver.py


## Creating the `app` and `db` Objects

Canonically, when using Flask and SQLAlchemy you'll create `app` and `db`
variables, usually in the following pattern:

    #!py
    from flask import Flask
    from flask.ext.sqlalchemy import SQLAlchemy

    app = Flask(__name__)

    #...

    db = SQLAlchemy()

    # ...

    db.init_app(app)

## The API Pattern

SQLAlchemy and Flask, at their boundaries, are both able to work with
dictionaries. In Flask, JSON message data can be accessed as a dictionary. In
SQLAlchmey, default contstructors for declarative-style classes accept a list of
keyword parameters (i.e. `**some_dict`). Given this, it's possible to whittle
away much of the repeated, boilerplate code required to create a simple REST API
for resources backed by database tables.

Let's start by thinking of the API for each resource as a micro-service. Each
service is distinct, both in code and in access patterns (i.e. you use different
URLs to access different "services"). 

Imagine we run an online music service and want to create a REST API 
for internal use. We can think of the endpoints we would likely need:

* /artists for CRUD operations related to artists
* /tracks for tracks
* /albums for albums
* /playlists for user playlists

Each of these can be thought of as it's own independent service, though 
they're all pretty similar in their operation. We should, then, be able to write
some generic "service" creation code that creates REST endpoints for a
SQLAlchemy table.

Let's look at what that might look like:
