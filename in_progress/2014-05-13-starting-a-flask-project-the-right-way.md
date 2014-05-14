title: Starting a Flask Project the Right Way
date: 2014-05-13 16:56
categories: python flask

One of my more popular series of posts has been [Starting a Django Project the Right Way](http://jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/).
As I've been working more and more with Flask, I've decided it's time for a
similar guide for Flask. This post will tell you what you need to start a proper
Flask project, how you do it, and things to watch out for/make your life easier.
By the end of it you'll have:

1. A fully working Flask application
1. All resources under source control (with git)
1. Automated regression and unit testing (using pytest)
1. An environment independent install of your project (using virtualenv)
1. Automated deployment and testing (using Fabric)

# Prerequisites

Before we start, let's make sure that we have the latest version of Flask. In
fact, we'll be using the latest verison of *all* packages. What happens if you
have other projects with dependencies on specific versions of packages being
installed? `virtualenvs` handle this problem nicely.

Using your "system python" (the Python distribution currently installed on your
system), download `virtualenv`:

    #!shell
    $ pip install virtualenv

Aaaaand that's the last time we'll touch your "system Python". Create a
directory for your project:

    $ mkdir awesome_project
    $ cd awesome_project

And now create a fresh virtualenv for your project:

    ~/awesome_project $ virtualenv awesome_project_env
    ~/awesome_project $ source awesome_project_env/bin/activate

You should see `(awesome_project_env)` in front of your shell prompt now. That's
just a reminder that your virtualenv is active and anything you install via pip
will only be visible to users of this virtualenv. To stop using the virtualenv
and go back to your system Python, simply type `deactivate` at any shell prompt.

## Install Flask

Now it's time to install Flask. Do so in the following way:

    (awesome_project_env) ~/awesome_project $ pip install flask

Let's add a simple file, `app.py`, to make sure everything is working properly.
Add a file in the `awesome_project` directory named `app.py` with the following
contents:

    #!python
    from flask import Flask

    Flask(__name__).run(debug=True)

That's the bare minimum Flask application, and if you've followed all the steps
correctly, typing 

    (awesome_project_env) ~/awesome_project $ python app.py

should give you the following output:

    * Running on http://127.0.0.1:5000/
    * Restarting with reloader

We can't actually browse to our application yet, but that will be rectified
shortly.

Let's create a requirements file using `pip freeze`:

    (awesome_project_env) ~/awesome_project $ pip freeze > requirements.txt

Now, we can recreate our environment from scratch in a new virtualenv if we need
to (say, in a deploy to another machine). **Each time you install a new package with `pip`, add it to `requirements.txt`.**
Letting this get out of date is a common source of headaches.

## Ctrl-S

We have performed a non-trivial amount of work, and it would be a shame to lose
it if, say, your disk died. Assuming you have a GitHub account, create a new
repo *without* a `.gitignore`. Run 

    (awesome_project_env) ~/awesome_project $ git init
    (awesome_project_env) ~/awesome_project $ git add .
    (awesome_project_env) ~/awesome_project $ git commit -m "Initial commit"

then add your GitHub repo as a remote using the second set of instructions on
your GitHub project's page:

    (awesome_project_env) ~/awesome_project $ git remote add origin git@github.com:<someuser>/awesome_project
    (awesome_project_env) ~/awesome_project $ git push --set-upstream origin master

Your GitHub page should now reflect the contents of your projct.

### Good Habits

Get in the habit of committing to git any time you've made a single, logical
change. That may be in only one file or across ten, but as long as all of the
changes are part of the same "logical" change, they should be committed
together. Also, *remember to `$ git push` often*, as `git` doesn't automatically
push to GitHub for you, and push-ing is the way that you sync your local commits
with the GitHub version of your repository.


