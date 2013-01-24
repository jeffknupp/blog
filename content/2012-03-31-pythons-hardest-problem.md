title: Python's Hardest Problem
date: 2012-03-31 08:03
categories: python GIL interpreter research

_For more than a decade, no single issue has caused more frustration or
curiousity for Python novices and experts alike than the Global
Interpreter Lock._

## An Open Question

Every field has one. A problem that has been written off as too difficult, too time consuming. Merely mentioning an attempt to solve it raises eyebrows. Long after the community at large has moved on, it is taken up by those on the fringe. Attempts by novices are undertaken for no other reason than the difficulty of the problem and the imagined accolades that would accompany a solution. The open question in Computer Science of whether P = NP is such a problem. An answer to the affirmitive has the possibility to literally change the world, provided a "reasonable" polynomial time algorithm is presented. Python's hardest problem is less difficult than crafting a proof of P = NP, to be sure. Nevertheless, it has not received a satisfactory solution to date, and the practical implications of a solution would be similarly transformative. Thus, it's easy to see why so many in the Python community are interested in an answer to the question: "What can be done about the Global Interpreter Lock?"

<!--more-->

## A Low Level Look at Python

To understand the GIL and its implications, we must start at Python's foundations. Languages like C++ are compiled languages, so named because a program is fed in to a compiler where it is parsed according to the language's grammar, transformed into a language agnostic intermediate representation, and linked into an executable comprised of highly optimized machine code. The compiler is able to optimize the code so aggresively because it is seeing the whole program (or large, self-contained chunks) at once. This allows it to reason about interactions between different language constructs and make informed decisions about optimization. 

In contrast, Python is an interpreted language. The program is fed into an _interpreter_ in order to be run. The interpreter has no knowledge of the program before it is run; rather, it knows the rules of Python and is capable of dynamically applying those rules. It too has optimizations, but optimizations of a rather different class. Since the interpreter cannot reason about the program proper, most of Python's optimizations are optimizations of the interpreter itself. A faster interpreter means faster program execution "for free". That is, when the interpreter is optimized, Python programs need not change to realize the benefit.  

This is an important point, so it bears repeating. The execution speed of a Python program, all other things being equal, is directly tied to the "speed" of the interpreter. No matter how much optimization you do within your program itself, your program's execution speed is still tied to how efficiently the interpreter can execute your code. It is clear, then, why much work has been devoted to optimizing the Python interpreter. It is the closest thing to a free lunch Python programmers can get.

## The Free Lunch Is Over

Or is it? A generation of programmers have learned to write code while Moore's Law was delivering hardware based speedups with predictable timing. If one wrote code that was slow, simply waiting a bit for faster processors was oftentimes the easiest solution. Indeed, Moore's law still holds true and likely will for quite a bit longer, but the _way_ in which it holds has fundamentally changed. No longer are clock rates steadily increasing to dizzying speeds. Instead, _multiple cores_ are used to take advantage of tranistor density increases. Programs wishing to capitalize on new processors must be rewritten to exploit _parallelism_.

When most developers hear "parallelism" the immediately think of multithreaded programs. Utilizing multiple threads of execution is by far the most common way to take advantage of multicore systems. While mulit-threaded programming is a good deal tougher than "sequential" programming, the careful programmer may nevertheless exploit parallelizable portions of his or her code to great effect. The implementation language should be an afterthought, since almost all heavily used modern languages support multithreaded programming.  

## A Surprising Fact

Now we come to the crux of the issue. To take advantage of multicore
systems, Python must support multiple threads of execution. Being an
interpreted language, Python's _interpreter_ must be written in such a way
so that doing so is both safe and performant. We all know the issues
that multithreaded programming can present. The interpreter must be
mindful not to operate on internally shared data from different threads.
It must also manage user's threads in such a way that the maximum amount of
computation is being performed at all times.

What, then, is the mechanism by which data is protected from
simultaneous access by different threads? The _Global Interpreter Lock_.
The name is instructive. Quite literally, it is a global (in the sense
of the interpreter) lock (in the sense of a mutex or simmilar construct)
on the interpreter. This approach is certainly safe, but it has (for the
new Python programmer), a startling implication: in any Python program,
no matter how many threads and how many processors are present, _only
one thread is being executed at any time_.

Many discover this fact by accident. Newsgroups and message boards are
littered with messages from Python novices and experts alike asking "why
does my newly multithreaded Python program run slower than when it had
only one thread?" Many feel silly even asking the question, since of course a
program with two threads where before there was just one will be faster
(assuming that the work is indeed parallelizable). In fact, the question
is asked so frequently that Python experts have crafted a standard
answer: "Do not use multiple threads. Use multiple processes." But this
answer is even more confusing than its question. I shouldn't use
multiple threads in Python? How can multithreading in a language as
popular as Python be so broken as to have experts recommending against
its use? Surely I'm missing something?

Sadly, nothing has been missed. Due to the design of the Python
interpreter, using multiple threads to increase performance is at best a
difficult task. At worst, it will _decrease_ (sometimes signifcantly)
the speed of your program. A freshman CS undergrad could tell you what
to expect when threads are all competing for a single shared resource.
The results are often not pretty. That said, there are many times that
mulithreading works well, and it is perhaps a testament to both the
interpreter implementation and the core developers that there are not more complaints
about Python's multithreading performance.

## What Now? Panic?

So what, then, can be done? Are we as Python developers meant to give up
the idea of using multiple threads to exploit parallelism? Why does the
GIL need to guarantee only one thread is running at a time anyway?
Couldn't finer-grained locks be added to protect individual objects from
simultaneous access? And why has no one attempted something like this
before?

These are useful questions with interesting answers. The GIL protects access to things like the current thread state and heap allocated object for garbage collection. There is nothing special about the Python language, however, that _requires_ the use of a GIL. It is an artifact of the implementation. There are alternative Python interpreters (and compilers) that do not make use of a GIL. For CPython, though, it's been there pretty much since the begining.

So why not get rid of it? Many are not aware, but this was attempted back in 1999 for Python 1.5 in the oft-cited but poorly understood "free threading" patches from Greg Stein. In the patches, the GIL was completely removed and replaced with finer grained locking. Its removal, however, came at the expense of execution speed for single-threaded programs. It was perhaps 40% slower when running with a single thread. Two threads showed an increase in speed, but beyond that the benefits did not scale linearly with the number of cores. Because of the degredation in execution speed, the patches were rejected and largely forgotten.

## The GIL is Hard. Let's Go Shopping!

The "free threading" patches are instructive, though, in that they demonstrate a fundamental point about the Python interpreter: removing the GIL is _hard_. Since the time of the patches, the interpreter has come to rely on _more_ global state, making the removal of today's GIL that much more difficult. It should be noted that it is precisely for this reason that many become interested in attempting to remove the GIL in the first place; hard problems are fun.

But perhaps this is all a bit misguided. Let's consider what would happen if we had a magical patch that removed the GIL with no performance penalty to single threaded Python code. We would have what we said we wanted all along: a threading API that properly makes use of all processors simultaneously. Now that we've got what we want, is it actually a good thing?

Thread based programming is hard. There are no two ways about it. Every time one thinks he or she understands everything there is to know about how threading works, a new wrinkle is uncovered. A number of high-profile language designers and researchers have come out against the threading model because it is simply too difficult to get right with any reasonable degree of consistency. As anyone who has written a multithreaded application can tell you, both developing and debugging are exponentially more difficult compared to a single threaded program.  The programmer's mental model, while well suited for sequential programs, just doesn't match the parallel execution model. The GIL, then, unintentionally serves to help protect a programmer from his or her self. While synchronization primitives are still required when using threads, the GIL actually helps preserve consistency of data between threads.
 
It seems, then, that Python's most difficult question may be asking the wrong thing. There's a good reason that Python experts recommend using multiple processes instead of multiple threads, and it's not to hide the inadequacies of the Python threading implementation. Rather, it is to encourage developers to use a safer and more straightforward concurrency model and reserve multithreaded programming for when it is absolutely necessary. To many, it is not clear what, if any, is the "best" model for parallel programming. What is clear to most, however, is multiple threads is not it.

As for the GIL, don't think it just sits there static and unanalyzed.  Python 3.2 saw a new GIL implementation by Antoine Pitrou with encouraging results. It was the first major change to the GIL since 1992. The change is too large to explain here, but at a high level, the old GIL counted Python instructions to determine when it was time to give up the GIL. As it turns out, a single Python instruction can comprise a large amount of work, as they don't translate 1:1 to machine instructions. In the new GIL, a hard timeout is used to instruct the current thread to give up the lock. When a second thread requests the lock, the thread currently holding it is compelled to release it after 5ms (that is, it checks if it needs to release it every 5ms). This leads to more predictable switching between threads when work is available. 

It is not a perfect change, however. Perhaps the most active researcher into the effect of the GIL on various types of work is David Beazley. In addition to what is likely the most in-depth look at the pre-3.2 GIL, he has researched the new GIL implementation and discovered a number of interesting program profiles for which even the new GIL performs quite poorly. He continues to drive the discussion surrounding the GIL forward with practical research and published results.

Regardless of one's personal feelings about Python's Global Interpreter Lock, it remains the language's most difficult technical challenge. To understand its implications requires a thorough understanding of operating system design, multithreaded programming, C, interpreter design, and the CPython interpreter implementation. Those prerequisites alone preclude many developers from investigating it more thoroughly.  Nevertheless, the GIL shows no signs of going away any time soon.  For the time being, it will continue to both confuse and surprise those new to the language while simultaneously intriguing those interested in trying to solve very difficult technical problems.

_The preceeding is based on my research to date into the Python interpreter. While there are many other parts of the interpreter I hope to write about, none is more well known than the Global Interpreter Lock. The technical details were researched thoroughly against the CPython repository tip, though I imagine there are some inaccuracies.  If you spot one, please let me know so that I may correct it as quickly as possible._
