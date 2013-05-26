## Yield, Asynchronous I/O, and Cooperative Multitasking

In the fist half of this post, we learned what the `yield` keyword does, why
it's useful, and how to use it. That post was the appetizer. This one is the
main course. Our entree selections? **Ansynchronous I/O** and **Cooperative Multitasking**.

### Asynchronous I/O

What is "asynchronous I/O," and why is it useful? Let's answer the second
question first. When the web was in its infancy, traffic was light. A web server
could handle the flow of *any* site using a "thread pooling" approach. In thead
pooling, a pre-defined number of threads are started when the web server starts.
Each time a request is received, it is passed off to one of the threads in the
pool to be processed. If a request comes in and all of the threads are already
busy servicing other requests, the web server "blocks", waiting for a thread to
become available. "Blocking", a term you'll hear a lot, is simply the practice 
of halting a program's progress until a certain resource becomes available. In
this case, the web server "blocks on" a processor thread becoming available.

As web traffic grew, thread pooling based web servers began to show signs of
strain. Many thought of threads as essentially "free"; if you had a problem that
was parallelizable, you simply created as many threads as you had processors and
your efficiency scaled linearly. Intuitively, this makes sense. Which of course
means it's wrong. There is a cost to distributing processing among threads:
*context switching*.

#### The kernel's secretary

In any modern OS, you're able to simultaneously run more programs than you have
processors. For example, a single dual-core processor can essentially do two
things at once. But it can't do any more than that. So how are you able to run
five programs (one of which is a browser with ten tabs open) as well as critical
OS processes? On Unices, the kernel's *scheduler* is responsible for magically
making it seem like far more things are running concurrently than is logically
possible.

You see, when you have five programs open, each is assigned a slice of time to
run based on a number of factors. Your program may run for 20 ms, then swapped
out for the next scheduled process (which may run for 50 ms), and so on until
it's your program's turn to run again. All of this happens so fast that it
*seems* like all of your programs are running at the same time (when things are
working properly).

Schedulers are tricky beasts to implement, and the Linux kernel has gone through
a number of them. The goal of the Linux scheduler is to generally function as
reasonably as possible under the miriad types of workloads seen on devices
running Linux. No small task. There are various ways to "help" the scheduler,
for example by setting a processes's niceness level (effectively communicating
what a processes's relative priority should be). One can even decide to use an
alternative scheduling algorithm or different scheduler alltogether.

#### And I care why?

So what does this have to do with asynchronous I/O? Remember that web servers
used pools of threads to manage multiple connections, assuming that creating
more threads led to free concurrency. But threads are *not* free. Each time the
scheduler decides to stop running one thread and start another, a *context switch* occurs.
The term "context switch" describes the work the scheduler must do when stopping
one process and starting another. Much like Python's generators in the previous
article, the state of the current process must be saved and swapped out, while
the previously saved state of the new process must be swapped in.

To be sure, context switches are *very* fast. In isolation. When you add more
threads or processes, though, you add more context switches. Additionally, each
thread gets its own stack (historically 2MB), so 512 threads would consume all
of the virtual memory on a 32-bit machine. While Moore's Law still held for 
CPUs, processor speed increases masked these issues. Then chip manufacturers began 
focusing on more, rather than faster, cores. Suddenly, the cost of all those context 
web servers were at a point where the cost of context switches, CPU cache ping-ponging, 
and thread stack size became so great that simply adding more threads wasn't an option. 

### The C10K Problem

The issue of serving ever increasing numbers of clients eventually became known
as the [C10K Problem](http://www.kegel.com/c10k.html). While kernel developers
added alternatives to venerable system calls like `select`, application
developers began exploring alternative styles of writing network code.
Asynchronous I/O emerged as an application-level solution: rather than spawning
hundreds of threads and putting the burden of scheduling them on the kernel, run
your process using a library that wrapped blocking system calls and accepted a
callback function to be run when the requested operation could be run without
blocking. A web server, for example, may ask to `read` on a socket and pass a
function that should be called when data is available. Instead of blocking on
that modified `read` call, the web server code continues to run, perhaps 
invoking the callback function of a previously requested `write` which is now ready. 
The key insight is that *all of this can take place in a single thread*, so
concerns about context switching and thread stack overhead dissapear.

#### A Different Style of Programming

Programs written to take advantage of asynchronous I/O naturally evolved to use a 
fundamentally different style of programming: *event-based programming*. While
imperative programs simply executed instructions in order, event-based programs
called possibly-blocking functions with a *callback function*. That is,
instead of waiting for a blocking function to return, they called a wrapped
version of the blocking function along with a function to be called when the
blocking function completed.

Though event-based program predates the web by a large margin, most application
developers had little experience with it. [Node](http://www.nodejs.org) is an
entire programming ecosystem created with the sole intention of exploring
language-level support for asynchronous I/O. As many a novice Node programmer
has learned, however, long chains of callback functions calling other callback
functions calling other callback functions (and so on) can be both confusing to
read/write and difficult to debug.


Both of t
If anyone has ever shouted "YOU SHOULD USE NODE FOR THAT," 

After [PEP 342](http://www.python.org/dev/peps/pep-0342/) enhanced the power
of `yield`, [PEP 380](http://www.python.org/dev/peps/pep-0380/) gave `generator`s the final piece of the puzzle: control over where they `yield`ed to. Instead of
`yield` always returning a value to the calling function, a `generator function`
could "delegate" its `yield` to another `generator` (called a `subgenerator`).

In practical terms, just like before we could `yield` the value
returned by a function call (e.g. `yield is_prime(10)`), we can now yield the
*value* returned by a subgenerator without worrying about if we're getting back
a proper value or a `generator object`.

This effectively means that multiple `generators` can create a sort of
symbiotic relationship, yielding back and forth between one another.
When might this be useful?

<a id="coro"></a>
## Coroutines, Asynchronous I/O, and Cooperative Multitasking

Let's implement a simple producer/consumer system.
In a typical implementation, we would use a queue available to
both `produce` and `consume`, each of which runs on a separate thread.
Here's an example (equivalent to our `produce` and `consume` description)
[from the Python documentation](http://:

    #!py
    def worker():
        while True:
            item = q.get()
            do_work(item)
            q.task_done()

    q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for item in source():
        q.put(item)

    q.join()

Becuase it is shared between multiple threads, access to the `Queue` must be synchronized.
In this case, it's straightforward because Python's
`Queue` class manages access internally. In the real world,
use of shared data between threads common. It is also a recipe for race
conditions, deadlocks, thread starvation, and all the other attendant issues
of multi-threaded code.

There's another way to implement a producer/consumer in Python, however.
Dave Beazly has [an excellent set of slides and examples](http://www.dabeaz.com/coroutines/) on using coroutines
to do (among other things) `cooperative multitasking`.  If we
implement `produce` and `consume` as coroutines, we avoid
the pains of multithreading. `produce` yields data to `consume` each time it is
called. `consume` simply yields until data is available, processes it, then
resumes waiting for data by yielding.

The scheduler takes care of managing the interaction between `produce`
and `consume`, but in a very generic way. It knows how to
dispatch `coroutines` and queue up `coroutines` to be run. It knows
nothing about what the tasks are actually doing (producing and consuming in this
case). **This is a powerful idea.** If we could write one "perfect" scheduler,
we could perform cooperative multitasking without needing to change our
programming paradigms.

Two interesting things to note here. Only one coroutine is executing at any
time, so data sharing issues disappear. Also, the execution pattern
of `consume` is the basis for a large number of asynchronous IO frameworks.
Like `consume`, work is done until some resource is required, at which point
the coroutine yields.

### Tulip: The Future of Asynchronous I/O in Python

Lack of first-party support for asynchronous I/O has hurt Python a bit, especially when
node.js showed how powerful it can be. It has been discussed quite frequently on
the python-dev dlist. Towards the end of last year, however, discussions about how asynchronous I/O
should be implemented in Python were all over python-dev. GvR created a number
of discussion threads exploring different approaches. Ultimately, he began a reference
implementation called . It's an
async I/O library that provides an event loop-and-callback style interface. This
is useful for interoperability with existing third-party async I/O frameworks
like Twisted and Tornado. But the BDFL (and many others)
aren't in love with frameworks that rely on callbacks.

As an alternative, there's a scheduler for `coroutine` based
asynchronous I/O and additional support from the library
(in the form of `Tasks`) for using `coroutines` with the event loop. The Tulip
library is a perfect example of how powerful the combination of
PEP 342's `send` and PEP 380's `yield from` can be.

Hopefully, this post has made it clear that `yield` can do far more than simple
iteration. Understanding `yield` at a fundamental level allows you to express
algorithms (especially those involving state machines) in an elegant and
easy-to-read way. And, after all, elegance and clarity are what we're after,
right?

[^1]: A refresher: a prime number is a positive integer greater than 1
nothing about what the tasks are actually doing (producing and consuming in this
case). **This is a powerful idea.** If we could write one "perfect" scheduler,
we could perform cooperative multitasking without needing to change our
programming paradigms.

Two interesting things to note here. Only one coroutine is executing at any
time, so data sharing issues disappear. Also, the execution pattern
of `consume` is the basis for a large number of asynchronous IO frameworks.
Like `consume`, work is done until some resource is required, at which point
the coroutine yields.

### Tulip: The Future of Asynchronous I/O in Python

Lack of first-party support for asynchronous I/O has hurt Python a bit, especially when
node.js showed how powerful it can be. It has been discussed quite frequently on
the python-dev dlist. Towards the end of last year, however, discussions about how asynchronous I/O
should be implemented in Python were all over python-dev. GvR created a number
of discussion threads exploring different approaches. Ultimately, he began a reference
implementation called . It's an
async I/O library that provides an event loop-and-callback style interface. This
is useful for interoperability with existing third-party async I/O frameworks
like Twisted and Tornado. But the BDFL (and many others)
aren't in love with frameworks that rely on callbacks.

As an alternative, there's a scheduler for `coroutine` based
asynchronous I/O and additional support from the library
(in the form of `Tasks`) for using `coroutines` with the event loop. The Tulip
library is a perfect example of how powerful the combination of
PEP 342's `send` and PEP 380's `yield from` can be.

Hopefully, this post has made it clear that `yield` can do far more than simple
iteration. Understanding `yield` at a fundamental level allows you to express
algorithms (especially those involving state machines) in an elegant and
easy-to-read way. And, after all, elegance and clarity are what we're after,
right?
