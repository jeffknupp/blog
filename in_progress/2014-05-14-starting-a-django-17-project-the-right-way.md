title: Starting a Django 1.7 Project the Right Way
date: 2014-05-14 08:48
categories: python django git fabric

*Back in February of 2012, I wrote an article titled ['Starting a Django Project the Right Way'](http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/), and later followed up with ['Starting a Django 1.4 Project the Right Way'](http://www.jeffknupp.com/blog/2012/10/24/starting-a-django-14-project-the-right-way/) and ['Starting a Django 1.6 Project the Right Way'](.  All of these articles still draw a consistent audience and are referenced in numerous StackOverflow answers, corporate wikis, and tweets. With the release of [django17.com](http://www.django17.com), I thought it appropriate to update this tutorial to reflect changes in Django with the new release.

The beginning of a project is a critical time, when choices are made that have long
term consequences. There are a number of tutorials about how to get started with
the Django framework, but few that discuss how to use Django in a professional
way, using industry accepted best practices to make sure your project's
development practices scale as your application grows. 
A small bit of planning goes a *long* way towards making your life (and the lives of any coworkers)
easier in the future.

By the end of this post, you will have

1. A fully functional Django 1.7 project
1. All resources under source control (with git)
1. Automated regression and unit testing (using py.test)
1. An environment independent install of your project (using virtualenv)
1. Automated deployment and testing (using Fabric)
1. A development work flow that scales with your site.

None of these steps, except for perhaps the first, are covered in the
official tutorial. **They should be**. If you're looking to start a new,
production ready Django 1.7 project, look no further.

<!--more-->

## Prerequisites

A working knowledge of Python is assumed. Also, some prior experience
with Django would be incredibly helpful, but is not strictly necessary.
You'll need [git](http://www.git-scm.com) for version control and a free
[GitHub](http://www.github.com) account. That's it!

## Preparing To Install

I'm assuming you have Python installed. If you don't head over to
[python.org](http://www.python.org) and find the install instructions
for your platform. I'll be running a 64-bit Arch server installation hosted by [Linode](http://www.linode.com/?r=ae1808f234f8e219de24842336fada09ef81d52f), with whom I'm very happy. (That link was an affiliate link, [here](http://www.linode.com) is one without the affiliate code).  

So, what's the first step? Install Django, right? 

*Not quite.*

One common problem with installing packages directly to your "system Python"
is that, if you have more than one Python project on your machine, 
you may run into dependency issues between your applications and the 
installed packages (since only one version of a packge can be installed and
anytime). For example, you may have a project that relies on version 
0.8 of the `requests` library, and another that relies on version 1.0. How do we satisfy both requirements without
disrupting all *other* projects? Either uninstall the problematic packages (*and* all of their dependencies) each time and reinstall the required version, or use virtualenvs. If you'd rather do the former, you can really just stop reading this right now. 
Using a virtualenv to manage a Python project is the recommended practice among
Python and Django users alike.

The base package itself, `virtualenv`, is great, don't get me wrong. But it can
be clumsy to work with. That's why I prefer to manage virtualenvs with the 
fantastic `virtualenvwrapper` package. If you're using pip to install packages
(and I can't see why you wouldn't), you can get both virtualenv and virtualenvwrapper by simply installing the latter.

    #!bash    
    $ pip install virtualenvwrapper

You'll then need to add a line to your `.bashrc|.zshrc` file to source the
`virtualenvwrapper.sh` file that was installed (check the `pip` output to see
where, but it's usually `/usr/local/bin/virtualenvwrapper.sh`). Once you
determine the location, add this line to your `.bashc|.zshrc` file:

    #!bash
    source /path/to/virtualenvwrapper.sh

## Creating a New Environment

Creating a virtual environment is simple. Just type

    #!bash
    $ mkvirtualenv <project_name>

So to start our project, which we'll call "whizbang", you would do:

    #!bash
    $ mkvirtualenv whizbang

You'll notice a few things happened:
  
*  `setuptools` and `pip` were automatically installed
* `(whizbang)` is prepended to your shell prompt

This is an extremely helpful part of virtualenv: it automatically
prepares your environment in a way that lets you start installing packages using
pip right away. The `whizbang` portion is a reminder that you're using a
virtualenv instead of your system's Python installation. To exit the virtual
environment, simply type `deactivate`. When you want to resume work on your
project, it's as easy as `workon whizbang`.

## Installing Django

"Wait, 'Installing Django'? I already have Django installed!" Fantastic.
You aren't going to use it. Instead, we'll install a fresh copy managed by our virtualenv
that can't be messed up by others (or yourself) working on the machine.
To install Django in your virtualenv, just type:

    #!bash
    $ pip install django
    
This should give you the latest version of Django (which will be installed in your
virtualenv area). You can confirm this by doing:

    #!bash
    $ which django-admin.py

This should point to your `$HOME/.virtualenvs/whizbang` directory. If it doesn't,
make sure you see `whizbang` before your prompt. If you don't, activate
the virtualenv using `workon whizbang`.

## The Source Code Time Machine

Before we actually start the project, we need to have a little talk. 
I've consulted on a number of Django/Python projects and spoken to hundreds of developers
in the last few years. Overwhelmingly, the ones having the most difficulty on
projects (of any size) are those that do not use any form of version control. It may sound unbelievable
given that we're living in the age of GitHub, but some developers have simply never been exposed 
to version control. Others think "this is a small project, version control is not necessary." **Wrong**.

**None of the tools or techniques listed here will pay greater dividends then the use of a version control system.**

I've gone back and forth in previous versions of this article between only
describing the use of git and describing both git and mercurial. I've decided
that the war is over, git won, and you should be using git for new projects
(especially if you intend to make them publicly available and expect people to
contribute).

Modern version control systems (VCS's) are *distrbuted*, meaning copies of the
entire repository (or "repo") are stored in multiple places. This is done both
for redundancy and becuase of the work flow it encourages. You'll be committing
to your *local* git repo, but you also need to be *pushing* to a central
repository. [GitHub](http://www.github.com) is an obvious choice here.
It's free to create an account and you're automatically given a number of 
repos to make use of.

If you need to learn more about git or GitHub, check out the git docs at
[git-scm.org](http://www.git-scm.org). [GitHub](http://www.github.com) also has
some great "getting started" documentation you can read.

## (source) Controlling Your Environment

Even though we haven't actually done anything yet, we know we're going to 
want everything under version control. We have two types of artifacts we're going 
to be committing: our code itself (including templates, css files, etc) and supporting
files like database fixtures, migrations (more on that later), and a
`requirements.txt` file. 

That last one, the `requirements.txt` file, is especially important. 
It lists the name *and version* of every package your project depends on.
From where does this information come? `pip`, of course! The `pip freeze`
command redirected to a file named `requirements.txt` (so `$ pip freeze > requirements.txt`)
is the standard way to create such a file.

But what good is it, you ask? It allows for the automated construction of your whole environment (without needing to remember and `pip
install` each package manually). You can go to any machine,
`git clone` your project, `pip install -r requirements.txt`, and your project
should be immediately runnable (minus database data, perhaps).

Let's go ahead and create our project directory. Use the `startproject`
command supplied by `django-admin.py` to get it set up. First, though, make sure
your shell is using the *right* `django-admin.py` file, the one in
`$HOME/.virtualenvs/whizbang/bin/django-admin.py`. Check that by typing

    #!bash
    $ which django-admin.py

(The `which` command shows the path to the supplied executable, telling which
one it will choose if it is available in multiple locations).

If it gives you a value other than the one mentioned above, make sure your
virtualenv is activated.

Now, to actually start the project:

    #!bash
    $ django-admin.py startproject whizbang

We'll see a single directory created: `whizbang`. Within the
`whizbang` directory, we'll see *another* `whizbang` directory
containing the usual suspects: `settings.py`, `urls.py`, and `wsgi.py`. At the same
level as the second `whizbang` directory is `manage.py`.

### Intermezzo: Projects vs. Apps

You may be wondering why, back in Django 1.4, the `startproject` command was added alongside the
pre-existing `startapp` command. The answer lies in the difference between
Django "projects" and Django "apps". Briefly, a *project* is an entire web site or 
application. An "app" is a small, (hopefully) self-contained Django application 
that can (but doesn't *have* to) be used in any Django project. If you're building a blogging application 
called "Super Blogger", then "Super Blogger" is your Django project. If "Super Blogger" supports
reader polls, "polls" would be an Django app used by "Super Blogger". The idea is that
your polls app should reusable in any Django project requiring
polls, not just within "Super Blogger". A project is a collection of apps, along with project specific logic. An 
app is a small logical grouping of functionality that may be used in multiple projects.

While your natural inclination might be to include a lot of "Super Blogger"
specific code and information within your "polls" app, avoiding this has a
number of benefits. Based on the principle of *loose coupling*, writing your
apps as standalone entities prevents design decisions and bugs in your project
from directly affecting your app. It also means that, if you wanted to, you could
pass of the development of any of your apps to another developer without them
needing to access or make changes to your main project. 

Like many things in software development, it takes a bit of effort up-front 
but pays huge dividends later.

## Setting Up Our Repos

Since we have some "code" in our project now (really just some stock scripts and
empty config files, but bear with me), now is as good a time as any to
initialize our repositories in source control. Here's how to do that in
git and Mercurial.

#### git

    #!bash
    $ git init

This creates a git repository in the current directory. Lets stage all of
our files to git to be committed.

    #!bash
    $ git add whizbang

Now we actually commit them to our new repo:

    #!bash
    $ git commit -m 'Initial commit of whizbang'

Let's also *push* our new repository to GitHub. Create a repo named `whizbang`
(public or private, doesn't matter). Don't worry about the other options, just
leave them unchecked. After you hit the "Create repository" button, it will take
you your repos home page. We'll be using the second set of commands listed there
(since we already have an *existing* repo on our local machine).

The first command below will tell git that there is a remote GitHub repo which
we'll refer to as `origin` and specifies its location. The second tells git that
`origin` should be considered "upstream" of our repository and thus have the
latest code at all times. When we do a `push`, we'd like to push the `master`
branch (git's default branch name) to the repo at `origin` (our Github repo).

From here on out, all that's required to synchronize your local repo and your
GitHub repo is a simple `$ git push`.

## Using Django 1.7's New Migration System

Prior to 1.7, one of the most frustrating aspects of Django was
managing changes to models and the associated changes to the database.
[South](http://south.readthedocs.org/en/latest/about.html) was the universally used
third-party package that made this process easier through the use of
"migrations". Luckily, Django merged the project's functionality into 1.7, so 
we don't have to do anything special to take advantage of database migrations.

By default, Django sets you up with an SQLite database, which is nothing more
than a single file. SQLite is quite useful for prototyping and is one of the most extensively
tested pieces of open source code that exist, but it's probably not what you
want to use on your production project. 

I recommend [PostgreSQL](http://www.postgresql.org/) as the database engine to
use on the project. You'll need to install postgresql locally (easily done on
Mac and Linux machines). You can then create a database for your project using
the `createdb` command like so:

    #!bash
    $ createdb whizbang

Check thtat the project is set up correctly using `psql`, the command-line
postgresql client, to connect to the new database:

    #!bash
    $ psql whizbang

Assuming you see the output above, you're database is all set up. You just need
to install a *driver* to allow Python to speak to it.

The most popular postgres driver for Python is `psycopg2`. Install it with `pip`
taking care to make sure your virtualenv is activated.

    #!bash
    $ pip install psycopg2

should do nicely.

You'll need to change the value of `DATABASES` in `whizbang/settings.py` to the
following:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'whizbang',
            'USER': os.getenv('USER'),
        }
    }

To check that all of our configuration is set properly, we'll perform the first
*migration* on the database. A *migration* takes the existing state of the
database schema and some directives to add to or change parts of it. It then
applies those changes, resulting in a database schema that mirrors the various models 
in your system, even if you decide to change something later.

The venerable `syncdb` command used to synchronize your models with the database
got the axe in 1.7. `migrate` takes its place (which makes sense given the new
emphasis put on migrations). Go ahead and perform your first migration (from a
fresh database to, well, *something*). Do so by using the `manage.py` script to
invoke the `migrate` command:

    #!bash
    $ ./manage.py migrate

You'll be prompted for a superuser name and password (which you can go
ahead and enter). More importantly, the tables used by Django internally have
been created and your application is at the minimum-viable state.

Since we've just made some pretty big changes, now would be a good time
to commit. You should get used to committing frequently, as the
more granular the commit, the more freedom you have in choosing
something to revert to if things go wrong.

To commit, lets see what has changed.

#### (git)

    #!bash
    $ git status
    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #       modified:   whizbang/settings.py
    #
    # Untracked files:
    #   (use "git add <file>..." to include in what will be committed)
    #
    #       whizbang/.settings.py.swp
    #       whizbang/__init__.pyc
    #       whizbang/settings.pyc

#### (Mercurial)

    #!bash
    $ hg status
    M whizbang/whizbang/settings.py
    ? whizbang/whizbang/.settings.py.swp
    ? whizbang/whizbang/__init__.pyc
    ? whizbang/whizbang/settings.pyc

You may notice files you don't ever want committed listed in the `git status`
output, like the compiled Python .pyc files and vim swap .swp files above. To ignore
these files, create a `.gitignore` file in your root project directory and add a shell 
glob pattern to match files you *don't* want to be tracked. For example, the contents 
of my file might be 

    #!bash
    *.pyc
    .*swp

Before we commit, we have one more piece of information to track: our installed
Python packages. We want to track the name *and version* of the Python packages
we're using so that we can seamlessly recreate our environment in our production
area. Helpfully, pip has a command that does exactly what we need.

    #!bash
    $ pip freeze > requirements.txt

I piped the output to a file called `requirements.txt`, which we'll add to
source control so we always have an updated list of what packages are being used.
The file *could* be given any name, but `requirements.txt` is the convention.

Let's stage and commit our settings.py and requirements.txt files to be committed by running 

    #!bash
    $ git add whizbang/settings.py requirements.txt
    $ git commit -m 'Set up database; performed first migration'

## New-Style Settings

As developers become more comfortable with Django and Python, they realize that
the `settings.py` file is simply a Python script, and can thus be "programmed".
One common pattern is for the `settings.py` file to be moved from the rather
curious project directory to a new directory called `conf` or `config` in the
project root directory. Or, if you prefer, you can change the `settings.py` file
to the `settings` *module* by making `settings` a directory and moving the
current contents into a file under that directory. You are then encouraged to
break your settings.py file into a series of files, one each for each
environment you use. Common settings are kept in a `base.py` file.

The rub is that an extra flag is passed to `manage.py` or `django-admin.py`
describing the location of your settings. You give it a dotted path, something
like `whizbang.settings.development`. That file, `development.py`, *first imports all common settings from `base.py` using `from base.py import *`*.
Then, any settings specific to "development mode" are placed in
`development.py` (`DEBUG = True`, anyone?).

#### Example

If you are a lone-developer and have only your local code
and the "real" code on your webserver, you would have `development.py` and
`production.py` files in your `settings` module along with `base.py` and an empty
`__init__.py` like this:

    #!py
    (whizbang) jknupp  ⓔ  whizbang  ~  whizbang  tree   master
    .
    ├── manage.py
    ├── requirements.txt
    └── whizbang
        ├── __init__.py
        ├── settings
        │   ├── __init__.py
        │   ├── base.py
        │   ├── development.py
        │   └── production.py
        ├── urls.py
        └── wsgi.py

Just be aware that you'll need to provide `--settings=whizbang.settings.<environment>`
to most `django-admin.py` and `manage.py` commands.

### Breaking INSTALLED_APPS

Regardless of how you set up your `settings.py`,`INSTALLED_APPS`can quickly grow into a morass of
third-party packages, in house django apps, and project specific apps. I like to
divide`INSTALLED_APPS`into three categories: 

* DEFAULT_APPS: Django framework apps installed as part of the default Django install (like the admin)
* THIRD_PARTY_APPS: Apps install from PyPI that live in your `requirements.txt` file
* LOCAL_APPS: The applications you create

This makes it much easier to see what third-party applications you're using and
what is home-grown. Just remember to eventually have a line similar to the
following:

    #!py

    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

Otherwise, Django will complain about not having `INSTALLED_APPS` defined.

## Creating Our App

Use `manage.py` to create an app named `pow` in the *new* normal way (`./manage.py
startapp pow`) and add it under `INSTALLED_APPS`. In 1.7, the Django
developers finally took my advice (*ahem*) and made `manage.py` executable by
default, which is why you can invoke it directly.

We'll add some gibberish models to the `pow` app to see what migrations look
like. Let's open `pow/models.py` and add the following:

## Our Development Area

A good habit to get into is to write and test your code separately from where
you're serving your files from, so that you don't accidentally bring down your
site via a coding error when you're adding new functionality, for example.
git and Mercurial make this simple. Just create a directory somewhere other than 
where `whizbang` is installed for your development area (I just call it `dev`). 

In your development (`dev`) directory, clone the current project using git or Mercurial:

    #!bash
    $ (git/hg) clone /path/to/my/project/

Both tools will create an exact copy of the **entire** repository. All changes,
branches, and history will be available here. From here on out, you
should be working from your development directory.

Since branching with both git and Mercurial is so easy and cheap, create branches
as you work on new, orthogonal changes to your site. Here's how to do it each tool:

#### (git)

    #!bash
    $ git checkout -b <branchname>

Which will both create a new branch named <branchname> and check it out.
Almost all of your development should be done on a branch, so that
`master` mimics the "production" (or "version live on your site") `master` and can be used for recovery at
any time.

#### (Mercurial)

    #!bash
    $ hg branch <branchname>

Note that branching is kind of a contentious topic within the Mercurial
community, as there are a number of options available but no "obviously correct"
choice. Here, I use a named branch, which is probably the safest and most
informative style of branching. Any commits after the branch command are done on
the <branchname> branch.

## Using Fabric for Deployment

So we have the makings of a Django application. How do we deploy it?
**[Fabric](http://www.fabfile.org)**. For a reasonable sized project, discussing anything else is a 
waste of time. Fabric can be used for a number of purposes, but it really shines
in deployments.

    #!bash
    $ pip install fabric

Fabric expects a *fabfile* named `fabfile.py` which defines all of the actions we
can take. Let's create that now. Put the following in `fabfile.py` in your project's root directory.

    #!python
    from fabric.api import local

    def prepare_deployment(branch_name):
        local('python manage.py test whizbang')
        local('git add -p && git commit') # or local('hg add && hg commit')

This will run the tests and commit your changes, *but only if your tests pass*.
At this point, a simple "pull" in your production area
becomes your deployment. Lets add a bit more to actually deploy. Add
this to your fabfile.py:

    #!python
    from fabric.api import lcd, local

    def deploy():
        with lcd('/path/to/my/prod/area/'):

            # With git...
            local('git pull /my/path/to/dev/area/')

            # With Mercurial...
            local('hg pull /my/path/to/dev/area/')
            local('hg update')

            # With both
            local('python manage.py migrate pow')
            local('python manage.py test pow')
            local('/my/command/to/restart/webserver')

This will pull your changes from the development master branch, run any
migrations you've made, run your tests, and restart your web server.
All in one simple command from the command line. If one of those steps
fails, the script stops and reports what happened. Once you fix the
issue, there is no need to run the steps manually. Since they're idempotent, you
can simply rerun the deploy command and all will be well.

Note that the code above assumes you're developing on the same machine you
deploy on. If that's not the case, the file would be mostly the same but would
use Fabric's `run` function instead of `local`. See [the Fabric documentation](http://docs.fabfile.org/) for details.

So now that we have our `fabfile.py` created, how do we actually deploy?
Simple. Just run:

    #!bash
    $ fab prepare_deployment
    $ fab deploy

Technically, these could be combined into a single command, but I find
it's better to explicitly prepare your deployment and then deploy as it
makes you focus a bit more on what you're doing.

## Setting Up Unit Tests

If you know anything about me, you probably know I'm crazy about automated
tests. Too many Django projects are written without *any* tests whatsoever. This
is another one of those things that costs a bit of time up-front but pays
*enormous* dividends down the road. If you've ever found yourself debugging
your app using `print` statements, having proper tests in place could have saved
you a lot of time.

For Django, the Python `unittest` module is perfectly sufficient. The following
is a minimal example of tests for a single app:

    #!py

    import datetime

    from django.test import TestCase
    from pow.models import Post

    class BlogPostTestCase(TestCase):
        def setUp(self):
            Post.objects.create(id=1, 
                title='Starting a Django 1.7 Project the Right Way', 
                date=datetime.datetime.now(),
                category='Django')
            Post.objects.create(id=2, 
                title='Python\'s Hardest Problem', 
                date=datetime.datetime.now(),
                category='Python')

        def test_posts_have_category(self):
            """Animals that can speak are correctly identified"""
            first_post = Post.objects.get(id=1)
            second_post = Post.objects.get(id=2)
            self.assertEqual(first_post.category, 'Django')
            self.assertEqual(second_post.category, 'Python')
            
You would put this code in a file called `test_<appname>.py` and place it in the
same directory as the app it is testing. To run the tests for an app, simply run
`./manage.py test <appname>`. The fabfile we created already knows to run the
tests before deployment, so no need to make any other changes.

### Enjoy Your New Django Application

That's it! You're ready to start your actual development. Now is when the real
fun begins. Just remember: commit often, test everything, and don't write code
where you serve it from. Regardless of what happens from here on out, you've definitely
started a Django 1.7 project the right way!
