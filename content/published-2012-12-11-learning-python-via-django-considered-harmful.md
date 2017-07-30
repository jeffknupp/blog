# Learning Python via Django Considered Harmful

I learned to program in Python indirectly. I was interested in learning about web application development and heard good things about Django. I didn't know Python, but the syntax and documentation looked straightforward enough. Like any reasonable programmer, I figured the language didn't matter and I would pick it up as I went.

Largely, this was true. Python proved to be quite learnable, and I was quickly productive on my Django project. It wasn't until long after the project was completed that I realized *I hadn't actually learned Python*. I had learned some odd mutant hybrid language: part Python, part Django. **Using Django to learn Python is a terrible way to actually learn Python.**
<!--more-->
In this post, we'll look at the official Django tutorial from a Pythonic perspective. By the end, you'll be convinced that programmers whose only exposure to Python is Django *do not really know Python*.

##Settings

`settings.py` is our first stop. The tutorial briefly mentions "It's a normal Python module with module-level variables representing Django settings." No one new to the language will understand the implications of this statement.

To a beginner, `settings.py` is just an oddly formatted configuration file. The fact that it is valid Python code, and that writing configuration files in pure Python can be a powerful tool, is likely missed. Because `settings.py` is devoid of any "normal" Python statements aside from creating dictionaries and lists, it's easy to miss that the file itself is written in Python. Personally, I didn't pick up on this until I was well into my first project. I didn't grasp its value until much later.

##Models

When it comes to Django models, the tutorial has this to say:

> "[models] are represented by simple Python classes. Edit the polls/models.py file so it looks like this:"

And goes on to show the following code.

    #!py
    from django.db import models

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField()

To begin with, both classes inherit from `django.db.models.Model`. Why?[^1]  There's no explanation of why this is necessary. Your "simple Python class" must inherit from our object, end of story. 

Then there's the field declarations. Have you ever written a non-ORM based class in Python that looked anything like the example? No `__init__` function, no reference to `self`. Heck, there aren't any instance attributes declared. Just a list of class attributes assigned to a bunch of cryptic Django field objects. In short, **this class looks unlike any Python class you'll ever write outside of Django**. (Unless it's an abstract base class)

There's a more important issue with the tutorial's treatment of models. For the sake of making Django's ORM approachable, **all 'data' in Django applications are encapsulated by a Class**. It's an unintentional message to new Python programmers: Python is object oriented everywhere; you should be too.

Of course, most experienced Python programmers use objects only when necessary. They 
prefer Python's built in data structures, especially when creating APIs.
Using native Python data structures is the closest thing to a
free lunch that exists with regard to program maintainability. I can't think of 
a single package I use regularly that encapsulates everything in a series of 
classes and forces the end user to do the same.

##URL Patterns

They're basically just a bunch of crazy configuration settings as far as the
user is concerned. What `urlpatterns` actually is (a list of lists,
tuples, and `RegexURLPattern`s, which are then further transformed for resolution) is remarkable in its unclarity (a new word). I'm skipping this section out of anger.

##Views

This is the example in the tutorial to map URLs to view functions:

    #!py
    urlpatterns = patterns('',
    url(r'^polls/$', 'polls.views.index'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    url(r'^admin/', include(admin.site.urls)),
    )

The fact that it uses the function names as strings makes my blood boil. For
novice Python programmers, learning that everything *really is* an object is
revelatory. When they finally understand that stuff like functions, classes (not just instances!), modules, and code objects can be passed as arguments, it's an amazing moment. They finally
begin to glimpse the purpose and power of "everything is an object." 

Django hides all of this by passing function names as strings, revealing none of
the power of Python's data model. The fact that the string even includes the relative import
path is face-slappery.

My favorite part of the views tutorial is the inclusion of the argument
`request` in example view functions. In all nine of the examples, it is neither
used nor mentioned once. A good lesson in design for novices...

##Wrapping Up

I'm stopping before the end of the tutorial because I'm unfairly bashing Django.
It's a fantastic project in every way I can think of, and the documentation 
is a great example of documentation done right. It's susceptible to my
criticisms because **it's not meant to teach you how to program in Python.**
Nevertheless, for many Django represents their first introduction to the
language. If you're looking for a great web framework in Python, look to Django.
If you're looking to learn Python, look somewhere else.

[^1]: It has to do with the way metaclasses are used by Django's ORM to provide syntactic sugar for the definition of models.
