## Revisiting "Python's Hardest Problem"

One of the first long-form articles I ever posted to this blog was a piece about
Python's *Global Interpreter Lock* entitled ["Python's Hardest Problem"](http://www.jeffknupp.com/PUTLINKHERE).
Two weeks ago, it was posted to [Hacker News](http://news.ycombinator.com) and sat
on the front page for a while, driving a lot of traffic to the blog. 

In the discussion on Hacker News, some commenters mentioned that I had neglected
to mention the various ways of working around the GIL. While that information 
didn't fit the purpose of the original article, it is nonetheless useful.
In this article, I'll describe the various alternative approaches 
to concurrency that the Python community has discovered/created. I hope this 
information is helpful to those who want practical advice for how 
to take advantage of concurrency in Python.

### Batteries Included: Multiprocessing

For many workloads for which the GIL is a bottleneck, one need look no further
than the Python standard library. The [multiprocessing](insert link here)
package trades threads for processes, to great effect. The idea is simple: if a
single instance of the Python interpreter is constrained by the GIL, one can
acheive gains in concurrent workloads by using *multiple interpreter processes*
in place of multiple threads. Helpfully, `multiprocessing` was written
with the same interface as the `threads` package, so code already using threads
doesn't require a massive rewrite to make use of multiple processes.

So how does it work in practice? One spawns a process in much the same
way that one creates a thread. The most visible difference between processes
and threads is their amount of access to shared data. An quick example is useful here.
Suppose we are writing a RSS feed reader and want to update our feeds with any new items.
We store the contents of our various feeds as a dictionary whose keys are 
the URL of the RSS feed and whose values are a list of that feed's entries.
When we "refresh" our feeds, we simply want to add new items to the end of the
associated feed list. 

This is clearly a parallelizable task. If we're using threads, we simply give
each thread a subset of the dictionary keys (i.e. feed URLs). For each key it 
receives, a thread will fetch new posts for that feed and append them to the
feed's list in our feed dictionary. We needn't be concerned with locking access 
to the feed dictionary since we know that each thread will be appending to 
independent lists. 

Using processes, the work is divided as before. Processes, however, 
don't share memory with the process that created them (unless explicitly told
to). Thus our child processes must shares data via messaging rather than shared 
access to the feed dictionary. The usual issues associated with multithreaded 
code (like data corruption, deadlocks, etc) are no longer a concern. Since no two 
processes share access to memory, there is no chance of concurrent 
modification. 

Well, that's mostly true. As it happens, there are two primary methods of
communication available in muliprocessing: `Queues` and `Pipes`. While 
the `Queue` class is internally synchronized and, thus, thread and process safe,
the `Pipe` class is not. If more than one thread or process attempts to read
from or write to the same end of a `Pipe` at the same time, corruption of data
may occur. To protect process-unsafe code, `multiprocessing` makes available 
the same synchronization primitives as `threading`.

Minor synchronization issues aside, all of this sounds great. That is, until we realize that 
sharing data via messaging requires us to make a *copy* of the data we'd 
like to share. In our example, the parent process would send a subset of the 
keys of our dictionary (i.e. the feed URLs) to each process. Copying the keys is not 
an expensive operation. However, the child processes must send back the contents of 
each feed's item list. If we have many feeds and few processes, the set of 
lists each child process must send to the parent process may be quite large. This 
means that the child process creates the large list and sends it to the parent, 
who must then make its own copy of the list.

In a pinch, one can make use of the state-sharing methods that `multiprocessing`
makes available: *shared memory* and *server processes*. Shared memory is
accessed through the `Value` and `Array` classes, and their names are indicative
of what they're used for. Alternately, the `Manager` class can be used to manage
access to shared state by way of *proxy* objects. The `Manager` 
