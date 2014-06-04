## Make a Website, From Start to Finish

Many tutorials about using Python and Flask to build a simple web application
assume a lot of knowledge on the part of the developer. In this post, I *won't*
assume you're familiar with HTML and CSS, but I *will* assume you've written at
least *some* Python. That said, we're going to build a website from start to
finish; from blank editor to deployed on a VPS, serving real traffic.

## Step 1a: Get a Domain Name

The first step doesn't involve writing any code: you need to acquire a domain
name. A "domain" is the text between "www" and ".com" in a website's URL.
Note that your domain needn't end in ".com" (in fact it may be cheaper if it doesn't),
it's totally up to you.  

Any reputable site that sells domains is fine. Make sure you're not
signing up for *hosting* as well as the domain name. There should be only one
charge and it should be between $5-$15, depending on the site you chose.
[name.com](http://www.name.com) is one I've used in the past, for whatever
that's worth.

## Step 1b: Get a VPS

The other thing you'll need, besides a domain name, is a *VPS*, or "virtual
private server". You'll need this to "host" your website. A server process
called a *webserver* will run on your VPS and serve traffic to your site.

Some may prefer a *PAAS* solution like Google App Engine or Heroku. 
That's fine (if you know what you're doing), but this tutorial will assume
you're going to use a Linux machine that you control to host your site.

Any VPS company is fine. My company, [straphost](http://www.straphost.com),
specializes in *teaching* you how to properly deploy more complex applications,
but would be fine to use (If you want to use
[straphost](http://www.straphost.com), I'll wave the up-front fee, so you'll
only pay the monthly amount). Other great sites to get a VPS from are
[linode](http://www.linode.com) and [Digital Ocean](http://www.digitalocean.com).
In both cases, the smallest server is fine. For the linux distribution, we'll
choose Ubuntu 12.04.

## Step 2: Create a Development Environment For Your Site

While we're writing the Python code that powers our site, we'll save the code,
HTML, CSS, and JavaScript code in a new directory. Name that directory anything
you'd like. Once you're in that directory, type `$ git init .` to initialize a
new, empty git repo.

### Create a `virtualenv`

Virtual environments are vital to the ongoing success of a Python project. A
virtual environment, or `virtualenv`, creates a completely new installation of
Python by copying or symlinking your existing Python interpreter. It
automatically installs a version of `pip` with will *only* install packages to
your `virtualenv`. This is helpful when you are working on multiple projects,
each of which depend on different versions of the same package. Creating a
`virtualenv` for each project is a fantastic habit to get into. 

If you don't already have it, install `virtualenv` using the `pip` package
manager: `$ pip install virtualenv`. *Create* a virtualenv for your site by
running `$ virtualenv venv` from you project directory. 

*Activate* your virtualenv by typing `$ source venv/bin/activate` from your project directory.
Your prompt should now have a `(venv) $` before it, indicating that your virtual
environment is active. To stop using your virtualenv and go back to the
system-installed Python, simply type `$ deactivate`. The `(venv) $` should
dissapear.

### Install Flask

Using `pip`, install [Flask](http://flask.pocoo.org) via `$ pip install flask`.
The command will also install all of Flask's dependencies. Make sure to do this
with your virtualenv activated or you'll install Flask to the system Python
rather than your new virtualenv.

Test that everything is working correctly by creating a file named `app.py`. The
contents should be as follows:

    #!py
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, world!'

    if __name__ == '__main__':
        app.run(debug=True)

Run the script by typing `$ python app.py`. You should see the following output:

    #!bash
    * Running on http://127.0.0.1:5000/
    * Restarting with reloader

You should now be able to point your browser to
[http://localhost:5000/](http://localhost:5000/) and see the message `Hello,
world!`. Believe it or not, you've just created an extremely simple web app!
Hit `CTRL-C` to stop the application.

Aside from `app.py`, Flask expects two other directories, `templates` and
`static`, to be created, so go ahead and do that now using `$ mkdir templates static`.
We'll discuss what should go in those directories in a bit.

## Step 3: Begin Application Development

We've arrived at the best part: actually writing our web application. So, what
will our application do? We're going to create a (somewhat) useful little app
that lets a user enter two US airports (with autocompletion). It then calculates the distance between
them and plots them on a beautiful, full-screen, Google Maps map. While small,
**this is a full and complete web application.**

### Download the data file

I scoured the internet for a list of US airports and their locations and
eventually found this: [us_airports.txt](http://www.jeffknupp.com/us_airports.txt).
Download that file and save it in the root directory of your project. If you
open the file, you'll notice it contains a good amount of data, most of which we
don't care about. All we are concerned with is the airport name, three-letter
code, latitude, and longitude.

### Parse the data file

Now that we have the locations of all US airports, let's add code to parse that
data and save it into a form that will be useful for us. Add the following code
to `app.py` (replacing the existing `@app.route('/')` ` and function definition):

   #!py

   # Store the latitude and longitude of each airport under its three-letter code
   AIRPORT_LOCATIONS = {}

   # Store the text we'd like to see during autocomplete for each airport,
   # keyed by *both* the full airport name and it's three-letter code (letting us
   # search for an airport with either piece of information.
   NORMALIZED_AIRPORT_NAMES = {}

   def load_airport_locations(filename):
   """Populate airport latitude and longitude data from given file.

   The list of US airports is short enough that we can simply read them in at
   startup and keep them in memory for the app's duration. If it were
   considerably larger we would use a database, but that's overkill here.
   """
   with open(filename, 'r') as file_handle:
       for line in file_handle:
           fields = line.split(',')
           name, code, latitude, longitude = fields[1].strip('\"'), fields[4].strip('\"'), fields[-5], fields[-4]
           AIRPORT_LOCATIONS[code.upper()] = (float(latitude), float(longitude))
           NORMALIZED_AIRPORT_NAMES[code.upper()] = ('{} ({})'.format(name, code), code)
           NORMALIZED_AIRPORT_NAMES[name.upper()] = ('{} ({})'.format(name, code), code)

Let's test our new function by commenting out the `app.run(debug=True)` line and
replacing it with:

    #!py
    load_airport_locations('us_airports.txt')
    print NORMALIZED_AIRPORT_NAMES['LAX']

You should see the following output:

    #!bash
    ('Los Angeles Intl (LAX)', 'LAX')

### Adding Tests

This sort of as-hoc testing is fine during development, but it shouldn't take
the place of real unit testing. 
