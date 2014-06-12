title: Flask Python Patterns
date: 2014-06-12 08:39
categories: python flask sqlalchemy

I've been working with [Flask](http://flask.pocoo.org)
(and [SQLAlchemy](http://sqlalchemy.org)) quite a bit, and
have noticed some patterns in each of the systems I develop.
Below is a list of best practices based on my experience.

# Project Layout

If you're creating a project called `whizbang`, start by creating a `whizbang`
directory in the top-level directory of your project. That is:

    > ~/projects/whizbang_project $ mkdir whizbang


## `runserver.py`

You'll need a file to actually run the application, so we'll create
`runserver.py` at the top-level directory of our project (not in the `whizbang`
directory we just created). Its contents are simple:

    #!py
    from whizbang import get_app

    app = get_app()

    if __name__ == '__main__':
        app.run()

We'll be creating the `app` in an *application factory*, which is why we are
importing a function called `get_app` from `whizbang`.

## `models.py`

Since I'm always using Flask-SQLAlchemy, I tend to have a `models.py` file that
lives inside the `whizbang` directory (in fact, all files discussed here, aside
from `runserver.py` should go in the `whizbang` directory). `models.py` is also
the file that contains our `db` variable, though it's not initialized there.
Lastly, of course, it contains database models.


## `__init__.py` and Application Factories

In the `whizbang` directory, create an `__init__.py` file. This is where you'll
create your `app`. Instead of creating it in the normal manner (`app = Flask(__name__)`),
we'll use an [*application factory.*](http://flask.pocoo.org/docs/patterns/appfactories/)

    #!py
    def create_app():
        app = Flask(__name__)
        
