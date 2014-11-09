title: Advanced Django Patterns To Keep Code DRY
date: 2014-11-09 09:44
categories: python django

Django developers often forget that what they're writing is just Python code.
Sure, it's very Django-specific and written in a Django-y style, but Django is
just Python. By keeping this in mind, it's possible to develop a number of time
saving patterns and general tools to keep your code as DRY ("*Don't Repeat Yourself*") as possible.

Most, if not all, of these patterns exist as third-party libraries. In my most
recent project, though, I forced myself *not* to use them in order to reaquaint
myself with Django after an extended hiatus. I'm reasonably happy with the
results, so I thought I'd share a few of the design patterns I found
particularly useful.

## CRUD

Django's sweet spot is *CRUD* (Create Read Update Delete) applications, where
models are being created, manipulated, and queried. While Django comes with a
good deal of support for CRUD operations in the form of generic view classes,
it's possible to take things one step further. I hate writing boilerplate code,
though, and using class-based views extensively usually requires a lot of
boilerplate code. You're constantly extending the view classes, adding a bunch
of endpoints to your URLs file, creating form classes, and writing a lot of
similar template code.

What I wanted was the ability to create a model, "register" it somehow, and
instantly have the create, update, delete, and detail pages generated
dynamically, including the view classes, URL routes, and even the HTML templates.
Is such a thing possible? Of course! This is Python, after all :)

### Generic Generic Views

To start, let's imagine we want to add a new model in the standard Django way.
First, we create the model definition in `models.py`:

    #!py
    class Post(models.Model):
        
