# Automatically Generate RESTful Endpoints From Your Flask-SQLAlchemy Models

I'm a bit obsessed with easily creating REST APIs using Flask. I've tried all
sorts of things, always trying to find the way that required the least amount of
effort from the end user. *Yesterday, I think I got as close as I'm going to get.*

<!--more-->

Enter `flask-sandboy`, a Flask extension for automatically giving your
Flask-SQLAlchemy models RESTful HTTP endpoints. "sandboy" is [sandman's](http://www.github.com/jeffknupp/sandman)
little brother, hence the name. They do similar things but are used for
different purposes.

## Tell me more...

When would you use `flask-sandboy`? Say you already have a Flask application
with a good number of models. Your front-end UI is great, but now you'd like to
offer a RESTful API as well. Rather than going through all your models and
creating new view classes (which would be *very* time consuming), just use
`flask-sandboy`.

**Using `flask-sandboy` only requires two lines of code (and one of them is an import)**

A sample `runserver.py` file for such an app may look like this:

    #!python
    from flask import Flask
    from models import Machine, Cloud, db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

And here is that same app with RESTful endpoints automatically created and managed by Flask-Sandboy

    #!python
    from flask import Flask
    from flask.ext.sandboy import Sandboy

    from models import Machine, Cloud, db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    sandboy = Sandboy(app, db, [Cloud, Machine])
    app.run(debug=True)

Simply by instantiating a `Sandboy` instance and giving it a list of classes,
you get a series of well thought-out RESTful HTTP endpoints. **It very well could serve as your project's entire REST API.**

## What's included

Of course, you don't *just* get a series of RESTful HTTP endpoints that return
proper status codes, you get request verification and pagination as well.

### Request verification

`flask-sandboy` automatically checks each request containing JSON data and makes
sure all required fields are present. If one is missing, it sends the proper
response code and includes the details about the missing field in the response.
It's pretty useful for preventing data corruption and as a front-line defense to
the database integrity checks.

### Pagination

Pagination of results comes for free as well. Simply add `/<model_name>?page=2`
to your request, and you'll get the second page with twenty results. In the near
future, you'll also get proper `Link` headers with pointers to the "previous
page" and "next page" URLs.

### Can I really use this?

Yes! `flask-sandboy` has 100% test coverage (as of right now). And it's only
going to get better/more stable as time goes by. The best part, of course, is
you never need to do any work to REST-ify your models (aside from those two
lines). Any upgrades will *just work* and shouldn't require any work on your
side.
