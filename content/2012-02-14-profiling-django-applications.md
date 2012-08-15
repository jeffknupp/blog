title: "Profiling Django Applications: A Journey From 1300 to 2 queries"
date: 2012-02-14 09:33
categories: python django profiling query
---

In this post, I'll discuss profiling Django applications through a case
study in [linkrdr's](http://www.linkrdr.com) code. Through the use of
profiling tools, I was able to reduce the number of database queries a
view was using from __1300__ to 2.

Introduction To Profiling
--------------------------------
At some point in most Django projects, some part of the application
becomes 'slow'. This doesn't have to be the case (more on that later),
but it's often the result of changes made without performance
in mind. 

In the begining, this is actually a good thing: __focus on
making it work first, then focus on making it fast__. Of course, you
don't want to code yourself into a corner by writing code that "works"
but does so in a way that it will _never_ be fast. Instead, you want to
keep performance in the back of your mind while implementing a solution
that makes sense. 

Once you've proven your solution works through your automated tests
([You are using automated tests, right?](http://www.jeffknupp.com/blog/2012/02/11/unit-testing-in-django/)),
the next step is to make sure its performance is acceptable. Note that
I didn't say 'optimal'. __Don't waste time making something faster than
it needs to be__. This should be common sense but, once the optimization
bug bites, it's common for developers to go a bit off the deep end and
keep trying to find optimizations long after it's necessary.
<!--more-->
So you're solution works, but it's slower than what you've deemed
acceptable. What's the first step? For far too many developers, it's

1. Fire up my editor
2. Take a look around 
3. Guess what I think is causing slowness
4. Make a bunch of changes
5. Hope it got faster

Wrong, wrong, wrong. If you take away one thing from the post, let this
be it: __developers are notoriously bad at predicting performance
bottlenecks__. People think, 'Well, I wrote it, so I should know what
could be causing slowness.' Instead of relying on faulty intuition, we should be relying on _data_.

Profiling is the process by which we accumulate data on the performance
of an application. This data can come in many forms, but usually is some
variation on reporting two things: the number of times a function or
line of code was executed and how much time it took to do so. For every modern
language there exist some form of profiling tools. Use them.

A Case Study
------------------------------
[linkrdr](http://www.linkrdr.com) allows, among other things, a user to
import their RSS/Atom/Twitter/Anything Else feeds and get an
inteligently laid out view of the _links_ contained in their feeds. The
`show_items` view for linkrdr is responsible for retrieving the user's
current feeds, gathering the links from those feeds' entries, and
scoring, sorting, and aggregating the links for presentation.

When I first began work on the view, I did so with a unit test prewritten.
I needed to get that test working, so I did so in the simplest way possible. Here's what
the code looked like:

<figure class="code">
<figcaption><span>Intial show_items implementation</span> 
```.python
def show_items(request):
    feeds = Feed.objects.filter(users__id=request.user.id)
    seen_links = {}

    class LinkScore():
        def __init__(self, link, score):
        self.links = [link]
        self.score = score

    for feed in feeds:
        for entry in feed.entry_set.all():
            for link in entry.link_set.all():
                # determine score for link

    sorted_links = sorted(seen_links.values(), key=lambda v: v.score,
            reverse=True)

    return render_to_response('links/entries.html', {'links': sorted_links, }, context_instance=RequestContext(request))
```

Simple, right? If someone asked you to write psuedo-code to perform this
task, I'm guessing it would look largely similar to this. Remember,
that's a good thing in the begining. We're focusing on correctness more
than performance.

This code turned out to be 'all right' in the performance department.
It eventually got on my nerves, though, becuase I knew it has a problem that experienced Django developers probably
spotted right away. Even though I was %99.99 percent sure I knew what
was slowing down this view, I approached optimizing this code the same
way I approach any optimization task. I began with profiling.

Profiling in Django is a little all over the map. There isn't really a
universally accepted solution, as you can tell by reading the
[Django wiki](https://code.djangoproject.com/wiki/ProfilingDjango). I've
been using
[django-extensions](https://github.com/django-extensions/django-extensions)
for a while now, and it has a very nice profiling feature: `manage.py runprofileserver`. It starts the Django webserver with the (now unmaintained but still useful) _hotshot_ profiler and writes a .prof profiling results file on every request. 
    
So I fired up the profile server and navigated to my view. A .prof file
was added to my /tmp directory. To interpret it, I entered the Django
shell and did the following:

<figure class="code">
<figcaption><span>Reading the profiling stats</span> 
```.python
import hotshot.stats

stats = hotshot.stats.load('/path/to/file.prof')
stats.sort_stats('time', 'calls') # sort the output based on time spent
in the function
stats.print_stats(20) # print the top 20 culprits
```

The result of this was as I expected:

<figure class="code">
<figcaption><span>Profiling output</span> 
```.bash
In [6]: stats.print_stats(20)
   557944 function calls (485997 primitive calls) in 3.959 seconds

   Ordered by: internal time, call count
   List reduced from 457 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1310    0.763    0.001    0.783    0.001 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/backends/postgresql_psycopg2/base.py:42(execute)
68656/15272    0.485    0.000    1.099    0.000 /usr/lib/python2.7/copy.py:145(deepcopy)
    67792    0.173    0.000    0.173    0.000 /usr/lib/python2.7/copy.py:267(_keep_alive)
     1310    0.152    0.000    0.155    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/backends/postgresql_psycopg2/base.py:116(_cursor)
     3818    0.136    0.000    1.294    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/sql/query.py:223(clone)
10041/5020    0.109    0.000    0.544    0.000 /usr/lib/python2.7/copy.py:234(_deepcopy_tuple)
     2344    0.089    0.000    0.106    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/base.py:275(__init__)
8838/7636    0.076    0.000    0.575    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/utils/tree.py:55(__deepcopy__)
    10258    0.067    0.000    0.072    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/utils/datastructures.py:110(__init__)
     1310    0.057    0.000    0.111    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:218(get_default_columns)
     3654    0.053    0.000    1.816    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/query.py:214(iterator)
     3280    0.050    0.000    2.209    0.001 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/fields/related.py:288(__get__)
21494/19090    0.046    0.000    0.356    0.000 /usr/lib/python2.7/copy.py:226(_deepcopy_list)
     5021    0.045    0.000    0.326    0.000 /usr/lib/python2.7/copy.py:306(_reconstruct)
     1310    0.044    0.000    0.420    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:47(as_sql)
     1310    0.040    0.000    0.069    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/sql/query.py:99(__init__)
     2620    0.037    0.000    0.099    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/sql/compiler.py:749(<lambda>)
     1310    0.037    0.000    0.846    0.001 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/backends/util.py:31(execute)
     3818    0.037    0.000    1.345    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/db/models/query.py:751(_clone)
    10258    0.037    0.000    0.037    0.000 /home/illest/linkrdr/virtualenv/local/lib/python2.7/site-packages/django/utils/datastructures.py:105(__new__)
```

As you can see, psycopg2 is calling `execute` 1310 times, which is
causing all sorts of slowness. Execute, in case you didn't guess, is the
function that executes an SQL query against the database. My view was
making __1310 database queries for a user with 4 feeds__.

Well, now we know what the cause of the slowness is. The question is: how do we fix it? I began by activating the django-debug-toolbar,
which lets you view the number of SQL queries a page generates, among
many other useful things. I confirmed that the number of queries
reported was the same in the debug-toolbar and went about optimizing the
code.

The first approach to optmization in Django should always be to modify the
problematic function without changing anything else. Sometimes, you won't be
able to optimize without making changes to your models or other parts
of your application, but this kind of change shouldn't be your first
inclination.

So I went back to my view and asked: is there a better way to get the same
data I'm currently getting? It turns out there is: using `select_related` in my query.
[select_related](https://docs.djangoproject.com/en/1.1/ref/models/querysets/#select-related) populates your QuerySet with the records you requested
plus related records based on ForeignKeys in your model. If I could
change my query to use select related, I could drastically reduce the
number of queries the view required.

There was an issue, though. My models were set up so that a Link
belonged to an Entry, which belonged to a Feed, which had a set of
Users associated. I had gone from the top down: a query filtering feeds
that belonged to the current user. What I needed to do to realize the
benefit of `select_related` was to get all of the objects I needed in
one query. Since what I really needed was `Link` objects, I changed the
query to:


<figure class="code">
<figcaption><span>Changing the query</span> 
```.python
links = Link.objects.select_related('entry', 'entry__feed', 'url', 'entry__url').filter(entry__feed__users__id=request.user.id)
```

This would give me all of the links that I was interested in, plus all
of the related objects that I'd be using. I reran the view profiling and
saw something unexpected: I was still performing over 600 queries. Using
the debug-toolbar to determine the lines of code generating these
queries quickly revealed my error. When using `select_related`, you must
make sure to _reuse the QuerySet in subsequent code_. If you
accidentally use a new QuerySet (even if the objects would have been in
the original QuerySet) it will result in a new database query. This
cascades down to any other objects using the new QuerySet, and now you've
got the same issue again.

After making sure I reused the QuerySet throughout my view and the
functions it called, I reran the view using the debug-toolbar. Finally I
had the results I wanted: all of the data generated in just 2 queries
(the other query was the User's Session query, which can't really be
avoided). One thing you need to be aware of when using `select_related`
is that the query can get so large as to be slower than the iterative
approach. That's something I'll definitely need to keep an eye on in the
future.

Cleaning Up
---------------------------

After re-running the tests to confirm my new code worked as expected and
committing the code to git, I had one more task left: update my unit
tests to reflect my new changes. While I didn't make any functional
changes, I did make performance changes, and __performance changes
should be unit tested just like functionality changes__. 

Helpfully, Django's `TestCase` class has an assertion `TestCase.assertNumQueries()`
that checks the number of queries performed during a test. I simply
added this assertion the my view test and I was done. This prevents me
from adding code in the future that increases the number of database
queries without forcing myself to decide if that's acceptable.

Questions or comments on _Profiling Django Applications_? Let me know in the comments below. Also, [follow me on Twitter](http://www.twitter.com/jeffknupp) to see all of my blog posts and updates.
