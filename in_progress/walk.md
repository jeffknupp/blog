# On Walking Before You Run

I've had the opportunity to lend assistance to a number of individuals
developing web applications in Python. Most of the time, the projects I help on 
are in the earlier stages of development (if development has even started). Most
of these projects turn out great. Those that don't, though, almost always suffer
from the same problem: the developer has decided to use a Python web framework but 
doesn't actually know Python. And the developers *know* he or she doesn't know
Python. They just figured they'd pick it up as they go.

For seasoned developers with experience in other programming languages *and*
with other web frameworks, this actually works (most of the time). It is those
new to programming and/or web development that eventually become overwhelmed by
the complexity of their project.

I've written about this (somewhat glibly) before, saying that learning Django is
a terrible way to also learn Python. But the issue is not specific to Django, or
even Python for that matter. **Creating a web application requires
three separate skill sets, and you can't learn them all at once.** At a minimum,
one needs to know:

1. The implementation language of the web framework
1. The basic anatomy of an MVC based web framework
1. Linux system administration, or experience with a service like Heroku or Google App Engine

I've worked with or spoken to scores of people looking to build a web
application but had no working knowledge of *any* of the topics above.
It's a frustrating experience for both parties, because their is so much
knowledge required *before the first line of code is written*.

I've been thinking about this problem for a while. I never want to discourage
someone from learning something new, but most don't realize the number of
domains in which knowledge is required to build a web application. The best
solution I've come up with thus far is to "shrink the problem space". If I can
teach one subject in a way that lays the ground work for the others, it will go
a long way towards helping someone continue making progress once I'm gone.

So what, exactly, am I advocating for would be web developers without 
the skills mentioned earlier? It's quite simple. **Before building a web application, one must build a working command line application with all of the desired functionality.** 
This means (initially) no messing with a database for persistence, 
no concern over what URL routing is or what problem templating systems 
solve.  Rather, one creates a pure Python
command line application in such a way that transitioning it to a web
application feels natural. Additionally, the web framework of choice will be
more understandable; its functionality mirrors the command-line application.
It simply makes some things a lot easier.

Let's walk through an example web application I'd like to create. As a private
tutor, I'd like a way to keep track of my scheduled sessions, payments for them,
and the creation of invoices.
