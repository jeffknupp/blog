title: "Starting a Django 1.4 Project the Right Way"
date: 2012-10-24 09:09
categories: django pip virtualenv fabric python deployment south
---

*Back in February, I wrote a post titled ['Starting a Django Project the Right
Way'](http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/),
which still draws a consistent audience eight months later. In those eight months,
Django has released version 1.4 of the framework, with 1.5 under active
developement and promising [experimental support for Python 3.x](https://www.djangoproject.com/weblog/2012/aug/19/experimental-python-3-support/). Given these
changes, as well as the availability of new and updated resources available to 
Django developers, I decided to revisit the concept of best practices when 
starting a Django project.*

The beginning of a project is a critical time. Choices are made that have long
term consequences. There are a number of tutorials about how to get started with
the Django framework, but few that discuss how to use Django in a professional
way, using industry accepted best practices to make sure your project *development* 
scales as your application grows. A small bit of planning goes a *long* way
towards making your life easier in the future.

By the end of this post, you will have

1. A fully functional Django 1.4 project
1. All resources under source control (with git or Mercurial)
1. Automated regression and unit testing (using the unittest library)
1. An environment independet install of your project (using virtualenv)
1. Automated deployment and testing (using Fabric)
1. Automatic database migrations (using South)
1. A development workflow that scales with your site.

None of these steps, except for perhaps the first, are covered in the
official tutorial. **They should be**. If you're looking to start a new,
production ready Django 1.4 project, look no further.

<!--more-->

### Prerequisites

A working knowledge of Python is assumed. Also, some prior experience
with Django would be incredibly helpful, but not strictly necessary.
You'll need [git](http://www.git-scm.com) or [Mercurial](http://mercurial.selenic.com/) for version control. That's
it!

### Preparing To Install

I'm assuming you have Python installed. If you don't head over to
[python.org](http://www.python.org) and find the install instructions
for your architecture/os. I'll be running on a 64-bit Ubuntu server installation hosted by [Linode](http://www.linode.com/?r=ae1808f234f8e219de24842336fada09ef81d52f), with whom I'm very happy.

So, what's the first step? Install Django, right? Not quite. One common
problem with installing packages directly to your current site-packages
area is that, if you have more than one project or use Python on your
machine for things other than Django, you may run into dependency
issues between your applications and the installed packages. For this
reason, we'll be using
[virtualenv](http://pypi.python.org/pypi/virtualenv) and the excellent
extentension [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) to manage our
Django installation. This is common, and recommended, practice among
Python and Django users.

If you're using pip to install packages (and I can't see why you wouldn't), you
can get both virtualenv and virtualenvwrapper by simply installing the latter.

~~~~~{.bash}    
$ pip install virtualenvwrapper
~~~~~

After it's installed, add the following lines to your shell's startup file
(.zshrc, .bashrc, .profile, etc).

    ~~~~~{.bash}
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/directory-you-do-development-in
    source /usr/local/bin/virtualenvwrapper.sh
    ~~~~~ 

Reload your startup file (e.g. ```source .zshrc```) and you're ready to go.

### Creating a new environment
Creating a virtual environment is simple. Just type

~~~~~.{bash}
$ mkvirtualenv django_project
~~~~~ 

where "django_project" is whatever name you give to your project.

You'll notice a few things happen right away:
* Your shell is prepended by "(django_project)"
* distribute and pip were automatically installed

This is an extremely helpful part of virtualenvwrapper: it automatically
prepares your environment in a way that lets you start installing packages using
pip right away. The "(django_project)" portion is a reminder that you're using a
virtualenv instead of your system's Python installation. To exit the virtual
environment, simply type ```deactivate```. When you want to resume work on your
project, it's as easy as ```workon django_project```. Note that unlike the vanilla
virtualenv tool, *where* you run these commands doesn't matter.

### Installing Django

"Wait, 'Installing Django'? I already have Django installed!" Fantastic.
You aren't going to use it. Instead, we'll use one managed by virtualenv
that can't be messed up by other users (or yourself) working elsewhere
on the machine. To install Django under virtualenv, just type:

~~~~~.{bash}
$ pip install django
~~~~~ 
    
This should give you the latest version of Django which will be installed in your
virtualenv area. You can confirm this by doing:

~~~~~.{bash}
$ which django-admin.py
~~~~~ 

Which should point to your ```$HOME/.virtualenvs/ directory````. If it doesn't,
make sure you see "(django_project)" before your prompt. If you don't, activate
the virtualenv using ```workon django_project```.

### Setting Up The Project

Before we actually start the project, we need to have a little talk. I've spoken
to a number of Django developers over the past few months and the ones having
the most difficulty are those that don't use a version control system. Many new
developers have simply never been exposed to version control. Others think that
since "this is a small project," that it's not necessary. **Wrong**.

*None of the tools listed here will pay greater dividends then the use of
a version control system.*

Previously, I only mentioned git as a (D)VCS. However, this project being in
Python, Mercurial is a worthy Python based alternative. Both are popular enough
that learning resources abound online. Make sure you have either git or
Mercurial installed. Both are almost certainly available via your distro's
packaging system.

If you plan on using git, [GitHub](http://www.github.com) is an obvious choice
for keeping a remote repository. With Mercurial, Atlassian's 
(Bitbucket)[https://bitbucket.org/] is a fine choice (it supports git as well, 
so you could use it in either case).

### (source) Controlling Your Environment

Even though we haven't actually done anything yet, we know we're going to 
want everything under source control. We have two types of 'things' we're going 
to be commiting: our code itself (including templates, etc) and supporting
files like database fixtures, South migrations (more on that later), and a
*requirements file*. In the old post, I recommended commiting your actual virtualenv,
but there are a few good reasons not to, not the least of which is it's
unneccessary. Using a requirements file gives you all of the benefits with none
of the overhead.

Let's go ahead and create our project directory. Use the new ```start_project```
command to get it set up.

Our current directory should show two directories: `env` and
`myproject`. Since we'll be tracking both of these in git, we'll
initialize our repository here using:

    $ git init

This creates a git repository in the current directory. Lets stage all of
our files to git to be committed.

    $ git add .

Now we actually commit them to our new repo:

    $ git commit -a -m 'Initial commit of myproject'

If you plan on using a service like Github or Bitbucket, now would be a
good time to push to them.

Using South for Database Migrations
-----------------------------------

One of the most frustrating things in a vanilla Django install is
managing changes to models and the associated changes to the database.
With the help of [South](http://south.aeracode.org), you can realistically create an entire
application without ever writing database specific code. Changes to your
models are detected and automatically made in the database through a
_migration file_ that South creates. This lets you both migrate the
database forward for your new change and __backwards__ to undo a change
or series of changes. It makes your life so much easier, it's a wonder
it's not included in the Django distribution (there has been some talk
of including a database migration tool in Django, but it hasn't happened
yet).

Still under our `(env)` virtualenv environment, install South like so:

    $ pip install south

We setup South by adding it to our INSTALLED_APS in the `settings.py`
file for the project. Add that now, as well as your database settings
for the project, then run `python manage.py syncdb`.
You'll be prompted for a superuser name and password (which you can go
ahead and enter). More importantly, South has setup the database with
the tables it needs.

You may have noticed that we just ran `syncdb` without having adding an app to the project. We do this first so that South is installed from the beginning. All migrations to our own apps will be done using South, including the initial migration.

Since we've just made some pretty big changes, now would be a good time
to commit to git. You should get used to committing frequently, as the
more granular the commit, the more freedom you have in choosing
something to revert to if things go wrong.

To commit, first add any untracked files:

    $ git add .

Git users may notice I'm not adding specific files but rather everything
under our main directory. That's becuase, to this point, _there isn't
anything we don't want to commit_. Let's commit our changes using:

    $ git commit -a -m 'Added South for database migrations'

Creating Our App
----------------

Use `manage.py` to create an app in the normal way (`python manage.py
startapp myapp`) and add it as an INSTALLED_APP. The first thing we'll do, before adding models, is
tell South we want to use it for migrations:

    $ python manage.py schemamigration myapp --initial

This creates a migration file that can be used to apply our changes (if
we had any) and also _revert_ them. We use the migration file to  _migrate_ the database changes (even though there are none)
using :

    $ python manage.py migrate myapp

South is smart enough to know where to look for migration files, as well
as remember what was the last migration we did. You can specify
individual migration files, but it's usually not necessary.

When we eventually make changes to our model, we ask South to create a
migration using:
  
    $ python manage.py schemamigration myapp --auto

This will inspect the models in `myapp` and automatically add, delete,
or modify the database tables accordingly.

Our Development Area
--------------------

One of the things you should get used to is doing development in a
separate area, not where you're serving your files from, for obvious
reasons. Git makes this simple and also helps with deployments.
Create a directory somewhere other than where `myproject` is installed
for your development area (I just call it `dev`). 

In your development directory, clone the current project using git:

    $ git clone /path/to/my/project/

Git will create an exact copy of the __entire__ repository. All changes,
branches, and history will be available here. From here on out, you
should be working from your development directory.

Since branching with git is so easy and cheap, create branches
as you work on new, orthogonal changes to your site. Do so by typing:

    $ git checkout -b <branchname>

Which will both create a new branch named <branchname> and check it out.
Almost all of your development should be done on a branch, so that
master mimics the current production master and can be used for recovery at
any time.

Using Fabric for Deployment
---------------------------

So we have the makings of a Django application. How do we deploy it?
Thanks to readers of the blog, I'm a recent convert to [Fabric](http://www.fabfile.org), a fantastic tool perfectly suited to our deployment needs. Install Fabric to our virtualenv like so:

    $ pip install fabric

Fabric expects a file , _fabfile.py_, to define all of the actions we
can take. Let's create that now. Put the following in your `fabfile.py`
in the `myproject` directory:


```.python
    from fabric.api import local

    def prepare_deployment(branch_name):
        local('python manage.py test myapp')
        local('git add -p && git commit')
        local('git checkout master && git merge ' + branchname)
```

This will run the tests, commit your branch change, and merge them into
master. At this point, a simple "git pull" in your production area
becomes your deployment. Lets add a bit more to actually deploy. Add
this to your fabfile.py:

```.python
    from fabric.api import lcd

    def deploy():
        with lcd('/path/to/my/prod/area/'):
            local('git pull /my/path/to/dev/area/')
            local('python manage.py migrate myapp')
            local('python manage.py test myapp')
            local('/my/command/to/restart/webserver')
```
This will pull your changes from the development master branch, run any
migrations you've made, run your tests, and restart your webserver.
All in one simple command from the command line. If one of those steps
fails, the script stops and reports what happened. Once you fix the
issue, there is no need to run the steps manually. Simply rerun the
deploy command and all will be well.

So now that we have our `fabfile.py` created, how do we actually deploy?
Simple. Just run:

     $ fab prepare_deployment
     $ fab deploy

Technically, these could be combined into a single command, but I find
it's better to explicitly prepare your deployment and then deploy as it
makes you focus a bit more on what you're doign.

Enjoy Your New Django Application
---------------------------------

That's it! You're ready to start your actual development. If you do a
lot of Django development, just dump all of the commands above into a
fabfile and make creating a proper Django app a one step process. I have
one which I'll upload to my github account later today. If you have any
questions or corrections, or think there's a tool/step I missed, feel
free to email me at [jknupp@gmail.com](mailto:jknupp@gmail.com) or leave
a comment below. [Follow me on Twitter](http://www.twitter.com/jeffknupp) to get all of the latest blog updates!
