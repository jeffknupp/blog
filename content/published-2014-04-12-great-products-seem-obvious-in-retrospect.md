# Great Products Seem Obvious in Retrospect

*Note, this page originally appeared on the [sandman.io](http://www.sandman.io) blog.*

**`sandman` automatically generates a REST API service and web admin from your existing database without requiring any code!**

When you look at the most disruptive technology products of the last few years
(or months, decades, etc), you may notice that the products themselves seem
"obvious". It's almost impossible to believe that there was a time when a
service like didn't exist. Or when to find out
what friends and family were doing we had to call them and ask. Or when a centralized place to share
videos didn't exist on the Internet.

<!--more-->
Dropbox, Facebook, and YouTube all share the same quality: *in retrospect, they seem obvious.*
In fact, some would say that they didn't actually *do* all that much. Personal
profile sites already existed. Wasn't it just a matter of time before someone made them pretty
and easy to use? And posting videos on the Internet was never difficult, so it's 
inevitable that *someone* would eventually create a centralized place for it.

In a way, it's true. These services took an existing (or "near-existing") 
technology and productized it. The key, though, is that Dropbox,
Facebook, and YouTube *fulfilled desires we didn't even know we had*. Each of
these web giants evoke a "that's it"-style shoulder shrug today, but they
noticed opportunities where no-one else did. They grew big by seeing need where
it didn't yet exist.

## Enter Sandman

[Sandman](http://www.sandman.io) (on [GitHub here](http://www.github.com/jeffknupp/sandman)) often evokes similar reactions when I describe it to people. "That's
it?" they wonder aloud. "Doesn't something already exist to do something like that?
Surely someone must have already done this. It seems so obvious!". Sandman,
which builds a web admin and REST API service on top of your legacy database
without requiring any code, *seems like such an obvious product that most people assume it already exists*. 
In fact, many people say that *they had the same idea*, but never followed
through.

To be sure, Sandman is no technological marvel. It takes two technologies which
are well established, ORMs (Object-Relation Mappers) and code generation, and marries them in a simple,
straightforward manner. The result, however, is nothing short of magic.

## Your Database, In Your Browser

I love the look on people's face when they first run Sandman. They enter the
details of their existing database, hit enter, and *bam!*, Sandman has opened a
browser tab pointed at their new admin site. There in front of them is all of
their data, waiting to be manipulated.

<img src="http://www.sandman.io/static/img/admin_small.jpg"></img>

For technical managers, other groups within the organization, and even external 
clients, the ability to add, edit, and delete information buried deep within an
enterprise database is unparalleled. Forget about clunky GUI tools that connect
to a single database and make you use SQL to add data. Just use your browser to
fill a simple form, where most data is already auto-filled for you, to make the
change to your data.

**"It's stored in a database," is a phrase that probably evokes a shudder from most technology managers and programmers**. With Sandman, hearing that something
is "stored in a database" is the same as hearing "you access that through a
beautiful, easy to use web tool that has been tested by hundreds of people".
Sandman really does "free" your data.

## Sandman Makes Things REST

When I'm showing Sandman to a developer, I ask them to `curl` a 
simple URL after they've connected Sandman. Without fail, their eyes light up when they realize the
clunky, over-complicated legacy database (the kind that exists in *every*
enterprise) now has a *super-clean* REST API. 

"Imagine how easily we can run custom reports," they say. "Better yet, we can have Sandman 
generate them on-the-fly and simply give our users the URL of the results!" 
Interacting with legacy databases in the enterprise will never be the same.

Rather than having to find and install drivers and write *different code* for 
each type of database they connect to, developers can simply program against a 
single, RESTful service using battle-tested open source libraries.
**The amount of code that Sandman makes redundant is shocking.** 
Sandman changes the way that developers create services, for the better.

## Surely This Already Exists!

By now, some readers are thinking, "Surely this technology already exists! It's
so obvious!" It does *now*. Sandman represents the effort required to marry ORMs
with code generation to **automatically, with no coding required** create a REST
API and web-based admin interface. Before Sandman, this "obvious" 
service *really didn't exist*. After Sandman, nothing will quite be the same.
