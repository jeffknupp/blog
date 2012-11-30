title: Building Your Second Django Site
date: 2012-02-08 05:03
categories: django python virtualenv fabric git
---

I started work on my second Django powered site today. It's not 
ready to be unveiled, but I've realized that, while your first site will
always be your baby, your second is where you start to hit your stride.

So what have I done differently? For one, __testing__. For
[IllestRhyme](http://www.illestrhyme.com) I never wrote any tests, which
has caused me no end of troubles. Now that the site is stable and
actively used, it's difficult to make myself go back and write tests,
though I know I need to. The new site has unit tests for
everything, and though it's somewhat of a pain to do, it will most
certainly pay dividends in the long run.

In the production environment, everything is running
under [virtualenv](http://pypi.python.org/pypi/virtualenv), Python's unofficial answer to the problem of running multiple
Python environments. It effectively does a clean Python install to a local
directory and hijacks `pip` and `easy_install` commands to install
packages locally. This guarantees packages for the new site don't clash
with packages for the old site.

Also, I'm using [Fabric](http://www.fabfile.org) for automating deployment tasks. While before I relied on a set of git hooks, this became a bit cumbersome. Fabric is fantastic for deployment. My fabfile backs up the site, downloads packages from git, creates symlinks, run South migrations, runs the tests, and reloads Apache. Deployment should really be a one-button-press activity. Fabric makes it easy. Thanks to a number of commenters (Alexis Bellido on this site, joelhaasnoot, spleeyah, jsvaughan, and marcofucci on Hacker News)  for pointing this out on a previous post.
<!--more-->
Still using Git as my DVCS, but now I've got 100s of commits to
a number of projects under my belt. This time around, git is a tool and
not a chore (the chore being actually learning it properly).

On the internals side, a lot of what I'm doing on the second site is in
pure Python (and some may eventually be in C++ libraries). Due to the nature of the site, storing everything in the
database would quickly lead to space issues, so much is generated
dynamically. For long-running tasks, I'm using
[Celery](http://www.celeryproject.org) and [django-celery](https://github.com/ask/django-celery). They're a breeze to work with. Tasks in Celery are basically fire and forget and the interface stays out of your way. 

If you were to look at my first site, you could almost tell the date a
file was written by reading the code. I was learning Django by doing,
and a lot of the early stuff is pretty rough. I've rewritten a lot of
it, but it's there. With the new site, I'm writing idiomatic Django (if there is such a thing)
from the start. Simple decisions like naming all of your views and
referring to them using `url my_view_name` were
made in the beginning, not halfway through the project when I first learned about them. After getting one large-scale Django site under your
belt, you should notice that the framework doesn't get in your way as
much. The boilerplate forms, views, and models come easy, leaving you
time and energy to work on the interesting stuff.

And it's the interesting stuff that should be the focus of your second
(personal) Django site. While a simple CRUD based application is a noble
goal for your first site, your second should push boundaries. My new
site has a whole host of interesting computational and optimization
problems, and those are fun to work on. Figuring out how to exclude a
field on a ModelForm for the first time is not.

One last thing. A number of people have asked me recently how difficult
it was to learn Django from scratch and take a site live, either out of
curiosity or because they've wanted to do the same thing. My answer:
the coding is easy; building something people want to use and getting
them to use it is hard. _Really hard_. It requires a totally different skill-set from
programming, but it's incredibly rewarding to even attempt. To anyone who's been toying
with the idea of launching a web site, as I had for years, I urge you to do so. The skills you
pick up in launching a site are invaluable and will positively impact 
your career. 

Questions or comments on _Building Your Second Django Site_? Let me know in the
comments below. Also, [follow me on Twitter](http://www.twitter.com/jeffknupp) to see all of my blog posts
and updates.
