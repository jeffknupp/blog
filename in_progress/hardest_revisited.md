## Revisiting "Python's Hardest Problem"

One of the first long-form articles I ever posted to this blog was a piece about
Python's *Global Interpreter Lock* entitled ["Python's Hardest Problem"](http://www.jeffknupp.com/PUTLINKHERE).
Yesterday, it was posted to [Hacker News](http://news.ycombinator.com) and sat
on the front page for a while, driving a lot of traffic to the blog. 

In the discussion on Hacker News, some commenters thought that I had neglected
to offer ways of working around the GIL. While that information didn't fit the
purpose of the original article, it is nonetheless useful to discuss. In this
article, I'll describe the various alternative approaches to concurrency the 
community has adopted. I hope this information is helpful to those who want
practical advice for how to take advantage of concurrency in Python.

### Batteries Included: Multiprocessing

For many workloads for which the GIL is a bottleneck, one need look no further
than the Python standard library. The [multiprocessing](insert link here)
package trades threads for processes, to great effect. The idea is simple: if a
single instance of the Python interpreter is constrained by the GIL, one can
acheive gains in concurrent workloads by using *multiple interpreter processes*
in place of multiple threads. Helpfully, `multiprocessing` was written to
emulate the interface of the `threads` package, so code already using threads
doesn't require a massive rewrite to make use of multiple processes.

So how does it work in practice? Much like with threads, one spawns a process
and shares data via communication rather than shared access to objects. The
usual issues associated with multithreaded code (like data corruption,
deadlocks, etc) are no longer a concern. Since the two processes do not share
access to data, there is no opportunity for concurrent modification.
