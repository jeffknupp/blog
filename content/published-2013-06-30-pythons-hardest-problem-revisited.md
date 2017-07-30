# Python's Hardest Problem, Revisited

One of the first long-form articles I ever posted to this blog was a piece about
Python's *Global Interpreter Lock (GIL)* entitled ["Python's Hardest Problem"](http://www.jeffknupp.com/blog/2012/03/31/pythons-hardest-problem/).
Two weeks ago, it was posted to [Hacker News](http://news.ycombinator.com) and sat
on the front page for a while, driving a lot of traffic to the blog. 

In the discussion on Hacker News, some commenters mentioned that I had neglected
to mention the various ways of working around the GIL. While that information 
didn't fit the purpose of the original article, it is nonetheless useful.
In this article, I'll describe the various ways the Python community has
discovered/created to mitigate the effects of the `GIL`. I hope this  information
is helpful to those who want practical advice for how  to take advantage of
concurrency in Python.
<!--more-->

## Batteries Included: Multiprocessing

For many workloads for which the GIL is a bottleneck, one need look no further
than the Python standard library. The [multiprocessing](http://docs.python.org/3.4/library/multiprocessing.html)
package trades threads for processes, to great effect. The idea is simple: if a
single instance of the Python interpreter is constrained by the GIL, one can
achieve gains in concurrent workloads by through *multiple interpreter  processes*
in place of multiple threads. Helpfully, `multiprocessing` was written
with the same interface as the `threading` package, so code already using
threads doesn't require a massive rewrite to make use of multiple processes.

How does it work in practice? One spawns a process in much the same
way one creates a thread. The most visible difference between processes
and threads is the amount of access to shared data they permit. A quick
example is useful here. Suppose we are writing a RSS feed reader and want to
update our feeds with any new items. We store the contents of our various feeds
as a dictionary whose keys are the URL of the RSS feed and whose values are a
list of that feed's entries. When we "refresh" our feeds, we simply want to
add new items to the end of the associated feed list.

This is clearly a parallelizable task. With threads, we would simply give
each thread a subset of the dictionary keys (i.e. feed URLs). For each key it 
receives, a thread will fetch new items in the associated feed and append  them to the
feed's item list in our dictionary. We needn't be concerned with locking
the feed dictionary since we know that each thread will be appending to
independent lists. 

With processes, the work is still divided as before. The default behavior
for processes,  however, is to not share memory with the process that created them. Global variables
are an exception to this, but if you're using global variables on a regular basis
we have much more important things to discuss. Our child processes must share data via messaging rather than shared
access to the feed dictionary. The usual issues associated with multithreaded 
code (like data corruption, deadlocks, etc) are no longer a concern. Since no two 
processes share access to memory, there is no chance of concurrent 
modification. 

Well, that's mostly true. As it happens, there are two primary methods of
communication available in multiprocessing: `Queues` and `Pipes`. While 
the `Queue` class is internally synchronized and, thus, thread and process safe,
the `Pipe` class is not. If more than one thread or process attempts to read
from or write to the same end of the same `Pipe`, corruption of data
may occur. To protect unsafe operations, `multiprocessing` makes available
the same synchronization primitives as `threading`.

Minor synchronization issues aside, all of this sounds great. That is, until we realize that 
sharing data via messaging requires us to make *copies* of everything we'd
like to share. In our example, the parent process sends a portion of the 
keys in our dictionary (i.e. the feed URLs) to each child process. Copying keys is not
an expensive operation. Retrieving the results is another matter.

Each child process must send back the contents of the set of item lists that were updated. If
we have many feeds and few processes, the resulting lists may be quite large (in terms of memory usage). Since no data is shared
between processes, clearly the parent process must copy the data a child process
sends to it. A workflow that includes copying data, possibly multiple times, is
not a recipe for an especially quick program.

To work around these limitations, one can make use of the two state-sharing methods that `multiprocessing`
makes available: *shared memory* and *server processes*. Shared memory comes
in the form of the `Value` and `Array` classes, and their names are indicative
of what they're used for. Updates to a `Value` or `Array` object will be immediately
visible to other processes with access to that object. Needless to say, proper
use of synchronization primitives is important when using shared memory.

Alternately, the `Manager` class can be used to manage
access to shared state by way of *proxy* objects. The `Manager` takes the data
to be shared and creates proxies of them. Code interacting with these
proxy objects is written as if it were interacting with the underlying data
itself. All access and modification of the proxy object, however, goes through the
`Manager`.

One advantage of the `Manager` over shared memory is that the
`Manager` need to reside on the same physical machine as the processes using
the proxy objects. Of course, that means that using a `Manager` is slower than
shared memory (even when everything is on the same machine).

Now, with the state-sharing methods provided by `multiprocessing`, we've
come full circle. The burden of managing synchronization when using  separate processes
for  concurrency essentially is place back on the developer. Once shared
state, is introduced, the developer is subject to all the attendant headaches
associated with multithreaded code.

But there's a silver lining: processes can make progress on multiple threads
of execution simultaneously. Since a parent process doesn't share the GIL with
its child processes, *all* processes can execute simultaneously (subject to the
constraints of the hardware and OS).

## PyPy

[PyPy](http://www.pypy.org) is often described as "a Python interpreter written in Python".
While that's a misleading description in a number of ways, suffice it to say that PyPy is an alternative implementation
of the Python interpreter that achieves (sometimes drastic) performance gains
 by using a JIT compiler (not unlike the JVM).
The PyPy implementation does not (as many mistakenly believe) do away with the `GIL`. It's still present and functions
much the same as the `GIL` in the cPython interpreter.

In August of 2011, Armin Rigo (a PyPy developer and the creator of [Pysco](http://psyco.sourceforge.net/)),
wrote a [post](http://morepypy.blogspot.com/2011/08/we-need-software-transactional-memory.html)
on the PyPy blog that generated quite a bit of discussion. In it,
he outlined a plan to add support for *Software Transactional Memory (STM)* to
PyPy. Software Transactional Memory (and *Hardware Transactional Memory (HTM)*)
treats modification of data as a *transaction*. A transaction is an atomic
operation; it either proceeds in it's entirety or is completely rolled
back. In PyPy's case, transactions encapsulate modification of Python
objects.

It's an idea that has been around for a quite a while,
but one that's receiving more  attention due to the planned introduction of  *Hardware Transactional Memory* into
general purpose CPUs (*some* of Intel's new Haswell CPUs have support for TSX,
Intel's extensions for HTM). In the most aggressive form of HTM,  there is no need to use
synchronization primitives to protect shared data. Each modification is recorded by the CPU; when a transaction finishes,
the CPU checks if anyone else made changes to the memory in question. If no
other modifications were made, the transaction succeeded and proceeds
normally. If a modification was detected, the transaction is rolled back and
and a "fallback" routine is executed. The fallback routine determines how
(and if) the modification should be retried.

This is a potential game-changer for multithreaded programming. As "Python's
Hardest Problem" described, multithreaded programming is difficult due to
both the cognitive load it burdens the developer with and the challenge in
debugging and proving the correctness of code. If the hardware (or software)
magically handled concurrent access to data without requiring anything from
the developer, multithreaded programming would be *much* easier.

But HTM remains quite experimental and hasn't yet gained traction. This is why,
back in 2011, Armin Rigo decided that STM was the the most promising avenue for
creating a "GIL-less" PyPy. Progress has been slow for the past two years
(for all the reasons that progress on any Open Source project is slow),
but there are signs this is about to change. In a [post](http://morepypy.blogspot.com/2013/06/stm-on-drawing-board.html) earlier this month,
Rigo cited a number of factors that would increase the pace of development
and included a number of ideas for optimizing the implementation.

The project's initial, stated goal was to include STM at a performance
penalty between 2x and 5x, with the intention of reducing (and eventually
eliminating) the penalty in subsequent releases. It remains to be seen if the
approach taken by Rigo and others is a viable one, but PyPy's STM project is
perhaps the Python community's best hope of C-based,
GIL-less Python interpreter.

## Alternative Python Implementations

While cPython is the official, "reference" interpreter implementation for the Python
language, there are a number of alternate interpreters written in languages
other than C. The two most popular are [Jython](http://www.jython.org) and
[IronPython](http://ironpython.net). Why are they of interest? **Neither has
a GIL.**

### Jython

Jython is a compiled Python interpreter written in Java. It is the successor to the
now defunct JPython project. The Jython project's focus, above all else,
is compatibility with cPython (tested using a slightly modified version of
cPython's extensive regression tests).

So how did Jython do away with the `GIL`? Actually, it wasn't a conscious
choice by the Jython developers. Because of the JVM's built-in garbage
collection, there is no need to copy cPython's reference-counting
implementation. Since there are no longer reference counts that need to be
modified on every object, we are free to remove the `GIL` (which is primarily
used for safe manipulation of reference counts on all `PyObject`s).

That's not to say that, when using Jython, one can ignore modification of
shared state *in one's own Python code*. The `GIL` doesn't protect one from
multithreaded *Python programs* (otherwise there would be no need for
`threading` to provide synchronization primitives). Rather,
it protects *the interpreter itself* from corrupting the bookkeeping data
associated with every Python object.

Still, with no `GIL`, Jython programs can take full advantage of all of the
cores on a machine (our "Holy Grail"). Jython, however,
is not without its drawbacks.

For starters, it does not support *any* C extensions. This is a deal-breaker for many people as a ton of popular Python
packages make use C extensions. Additionally, development and feature support
lag well behind cPython. The *beta* for Python 2.7 was released in February
of this year (and has not seen a release since). Python 2.5 is the officially
supported version of Python in Jython. For reference,
2.5 was released **September 2006**. So it's fair to say that compatibility
is a very real problem for Jython.

Lastly, there a number of areas where Jython (by its own admission) is slower than cPython. Any Python standard
library modules written in C (and there are a lot of them),
Jython implements in Python. These could be rewritten in Java,
but the amount of optimization done cPython's C-based modules is pretty
extensive. Jython is unlikely to approach the speed of cPython modules
written in C any time soon.

### IronPython

Just as Jython is a compiled Python interpreter written in Java,
IronPython is a compiled interpreter written in C#, making it compatible with
the rest of the .NET ecosystem. Much like Jython, the `GIL` is rendered
unnecessary due to the .NET DLR's garbage collector. Also like Jython,
IronPython benefits from a JIT compiler to achieve speedups in longer running
programs.

While IronPython programs can take full advantage of multicore hardware,
the drawbacks of IronPython are largely the same as those of Jython. C
extensions are somewhat supported using "IronClad",
a commercial tool developed by Resolver Systems. This support only extends to
Python 2.6 extensions on (increasingly rare) 32-bit Windows systems, though,
and no code has been committed to the project since 2011. I think it's fair
to say that C extensions are basically unsupported (especially in the 2.7
version of IronPython).

Again, performance is a mixed bag. While the JIT compiler give IronPython a
leg-up in certain areas, there are many areas in which IronPython is
considerably slower than cPython (especially the built-in data structures that
are written in highly-optimized C for cPython). Whether or not your code
will run faster or slower on IronPython depends heavily on your workload.

### Missing the forest for the trees

Our discussion of IronPython and Jython has focused on the fact that neither
implementation has a `GIL`, but that's really of little interest to most
developers using either of them. Both projects were created not to merely implement the cPython interpreter in
another language, but to allow Python code to interact with other parts of
each interpreter's ecosystem. Calling Java code from Jython is straightforward.
To companies and individual developers operating in a Java-centric
environment, this is a huge win. Likewise, IronPython allows Python code to
interact with the rest of the .NET ecosystem.

So while neither is likely to become the reference implementation for Python,
that wasn't the goal of either project to begin with. It's not fair to judge
them on their speed or knock their compatibility with C extensions. That was
never their goal. Truly, they are both incredible projects that have been
wildly successful at accomplishing what they set out to do. Most
"vanilla" Python developers won't use alternate interpreters to increase
performance of multithreaded code. *And that's just fine.*

## Third Party Libraries

There are a number of libraries that extend the capabilities of the cPython
interpreter in some way. **None, to my knowledge, affect the GIL in any way.**
Many people are under the assumption that [Stackless Python](www.stackless.com)
has somehow removed the `GIL` (it hasn't). The same goes for [eventlet] (http://eventlet.net),
[greenlet](greenlet.readthedocs.org), [Twisted](http://twistedmatrix.com/trac/),
[gevent](http://www.gevent.org), and [Tornado](http://www.tornadoweb.org/en/stable/)
(all of which I've been mistakenly told at some point have no `GIL`). Some of
these packages and frameworks help alleviate the pain associated with the
`GIL`, but all are subject to its limitations.

## In Summary

When I originally wrote ["Python's Hardest Problem"](http://www.jeffknupp.com/blog/2012/03/31/pythons-hardest-problem/),
my goal was to introduce Python novices to the `GIL`,  explain its function,
discuss a bit of its history. "Hardest" in the title was meant to be
interpreted as "most technically challenging," not "most important" or "most
interesting to everyday programmers," but that's not how a
number of people took it. This is surely due to a lack of clarity on my part,
but I hope that this post will help rectify that. There are likely a number
of approaches/tools to dealing with the `GIL` I did not mention here. Feel
free to point them out in the comments.

My goal for this post is to enumerate a number of ways the community has
dealt with the issues the `GIL` presents for novice Python programmers. If
you feel any of the information above is incorrect or misleading,
please let me know in the comments or [via email at jeff@jeffknupp.com](mailto: jeff@jeffknupp.com).
