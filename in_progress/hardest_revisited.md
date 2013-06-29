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

## Batteries Included: Multiprocessing

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

Using processes, the work is divided as before. The default behaviour for processes, 
however, is to not share memory with the process that created them. Global variables
are an exception to this, but if you're using global variables on a regular basis
Thus our child processes must shares data via messaging rather than shared 
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
sharing data via messaging requires us to make *copies* of the data we'd 
like to share. In our example, the parent process sends a portion of the 
keys of our dictionary (i.e. the feed URLs) to each child process. Copying keys is not 
an expensive operation. Retrieving the results is another matter.
The child processes must send back the contents of each feed's item list. If we have many feeds and few 
processes, the resulting lists each child process must send to the parent 
process may be quite large (in terms of memory usage). Since no data is shared
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
you want to be shared and creates proxies for them. To code interacting with these
proxy objects, they appear identical to the underlying data being shared. All
access and modification of the proxy object, however, goes through the
`Manager`. One advantage of the `Manager` over shared memory is that the
`Manager` need to reside on the same physicall machine as the processes using
the proxy objects. Of course, that means that using a `Manager` is slower than
shared memory (even when everything is on the same machine). 

And now, with the state-sharing methods provided by `multiprocessing`, we've
come full circle. The benefits of using separate processes for concurrency
vanish. Once we introduce shared state, we are subject to all of the headaches
associated with multi-threaded code. 

But there's a silver lining: we can actually make progress on multiple threads
of execution simultaneously. Since a parent process doesn't share the GIL with
its child processes, *all* processes can execute simultaneously (subject to the
constraints of the hardware and OS).
