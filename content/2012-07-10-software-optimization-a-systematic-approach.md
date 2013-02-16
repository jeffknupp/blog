title: Software Optimization: A Systematic Approach
date: 2012-07-10 05:25
categories: software optimization linux c++


## Introduction ##

What follows is the first in a series of articles on developing a formal methodology 
for software optimization I've been working on for some
time. Each week, I'll post the newest installment here (they're all written, I'm just
wary of dumping the whole thing here all at once). Feedback is of course welcome and
encouraged. The complete version will be available in epub format, as well as online
in a more readable style. I hope you enjoy reading this half as much as I enjoyed
writing it.

## Part 1: A Primer ##

Software Optimization is a topic which receives a curious lack of coverage in
most Computer Science curricula. Even on the Internet, there are few resources
which approach the topic in any kind of structured manner.  Typically, a
programmer blogs about how they made a certain piece of code x times faster and
describes the series of changes made. These "optimization anecdotes" are
entertaining but rarely useful as a way to learn how to optimize one's own code.
*The main problem in learning how to optimize code is that no one is actually
teaching it.*

Especially in the enterprise, optimization is poorly understood by many developers. There are a number
of reasons for this: lack of understanding about OS level operations, lack of familiarity
with tools to aid optimization, and the difficulty in correctly anticipating bottlenecks
in one's code, to name a few. Junior developers, lacking the proper experience
to even know where to start, often practice cargo-cult optimization, applying
optimizations they've seen or read about elsewhere without determining if they're impactful and
appropriate. 

_It's time the practice of software optimization had a homepage._ 

This series of articles will present a formalized, structured approach to
software optimization. While most of the examples will focus on Linux, the
methodology and ideas are universally applicable. A programmer on any other
OS should have no problem following along and get just as much
out of it. An embedded systems developer will find the low level details
different but the approach the same.

<!--more-->

### Reality Check ###

This is the part where I'm supposed to tell you that after reading this series
you'll be ready to amaze your boss by fixing all of the slow-performing 
code in whatever it is you work on. Unfortunately, that won't be the case. I must be
very clear about this point lest anyone have unreasonable expectations: Even
after reading this entire series and all of the background material mentioned,
becoming a skilled practitioner of optimization will likely require at least ten
years of professional development experience and at least two to three years
working on a performance critical system. It is not a skill one picks up all at
once; rather, it draws on the knowledge built over one's career.
The study of optimization is not done in isolation. It necessarily includes a
wide variety of domains such as OS interaction, hardware design, high performance data
structures and algorithms, and testing methodologies.

But there's a very bright silver lining. _I know of no better way to become a
better programmer than to study optimization_. The knowledge you pick up along
the way about topics you don't encounter in your day to day work
will benefit you the rest of your career. You'll write better
code, design more coherent systems, find and fixing bugs more quickly, and
perhaps most importantly, be able to think critically and reason about software
systems.

And now, we begin...


### Lesson 1: Building a Foundation ###

To effectively optimize code across a variety of domains, you need to become a technical
renaissance wo/man. There's no way around it: optimization takes at least a general understanding
of a _lot_ of different areas of computing. Below are areas of particular interest. 

#### Hardware for Software People ####

Many developers have an aversion to learning about hardware. Get over it. You'll need a good
background in the topics below to be truly effective at low-level optimizations. All of them
are far too broad to cover adequately here. For the topic of caching, because of how often if affects 
performance, I've included summaries of relevant information mostly aimed at refreshing the knowledge 
of those already familiar. 

##### Memory #####

###### Recommended Reading ######
The seminal modern work on Linux memory is surely libc maintainer Ulrich Drepper's [What Every Programmer Should Know About Memory](http://lwn.net/Articles/250967/).  Honestly, There's not much he doesn't cover, so this is it for recommended readings.

###### Cache architectures ######
Modern CPUs have on die memory in order to facilitate caching, typically used to cache the contents of recently read or written values. The basis for singling out recently used values is the principal of _temporal locality_ which states that, all things being equal, a resource used recently is likely to be needed again soon. Since access to system memory is comparatively expensive, caches operate not on individual addresses but "cache lines", fixed size chunks of memory representing contiguous physical memory. Based on the idea of _spatial locality_, or that a resource physically close to one recently used will likely be used soon, caching memory in chunks has the added benefit that most programs access data reasonably sequentially. While the cache is meant to benefit programs without their needing to explicitly attempt to make use of it (or, indeed, even know of its existence), it can also play an adversarial role in low-level optimizations. Designing programs that work with the CPU's cache is critical to good performance in highly optimized routines.

###### Cache Coherence ######
Multi-processor (and multi-core) architectures naturally require a consistent view of memory across all processors. Otherwise, threads running on different CPUs making a change to the same memory address could create an inconsistent state by setting their copy of the same element to different values. To compensate, CPU architectures implement _cache coherency protocols_ using a variety of methods. Often, reading and writing have separate rules governing the actions that must be performed after the operation completes. The protocols differ not just between CPU manufacturers but between CPU families as well, making it somewhat difficult to make generalizations about "modern" cache coherency. That said, the information is widely available for most commercial processors and the implementation is usually based on one of a number of well-understood algorithms. When optimizing for memory access patterns, one must be mindful of how multiple threads on different CPUs operating on shared data can be _less_ efficient than a single thread performing the same work because of cache coherency issues.

###### False sharing ######
Related to coherency, false sharing occurs when one thread writes and one or more threads read from logically separate areas of memory that happen to occupy the same cache line. These addresses in memory need not be related to one another in the host program (though their short distance usually means they are in some way). When the threads are running on the same core this is not a problem. When running on different cores, however, each write performed by one thread invalidates the cache line the readers are accessing. The effects of false sharing even on extremely simple programs can be dramatic. Herb Sutter has a great article [Eliminate False Sharing](http://www.drdobbs.com/go-parallel/parallel/eliminate-false-sharing/217500206) that covers the topic with simple examples.

###### Ping-Ponging ######
When false sharing occurs with a frequently used memory location, the valid cache line will effectively bounce back and forth between the cores involved. This is known as "ping-ponging" or "thrashing". Of course, ping-ponging need not be caused by false sharing. Any access pattern that results in multiple resources competing for the same cache line will exhibit this behavior.

##### CPU #####
* CPU pipeline
* Instruction cache
* Branch prediction
* Logical versus physical cores (or why you're dual core CPU reports more than two cores)
* Extended instruction sets

##### Disk #####
* Relative access speed

#### Know Your OS ####
You should try to understand your target OS as intimately as possible. Different Linux kernel versions
can vary a great deal in implementation efficiency of both kernel and user space operations. For the same
reason, you should also be familiar with the particular version of the Linux distro you're running.
A good way to learn about what's slow in your kernel or Linux distro is to read the 
change notes for all releases _after_ the one you're using. You'll see bugs the developers
fixed as well as operations they optimized. In addition, they'll normally have an 
article or series of emails describing the change by first giving background as to why it's slow. This
will help you anticipate possible sources of slowness.

The list below is a good overview of topics important to optimization in general.

###### Virtual Memory ######
* Implementation
* Cache interaction

###### Atomic Operations ######
* Implementation 

###### Threading ######
* Synchronization primitives
* Context switching
* Scheduling

###### User Space vs Kernel Operations ######
* Affect on thread scheduling

###### IPC ######
* System V vs POSIX shared memory
* UNIX domain sockets
* Memory mapped files
* Implementations

### Lesson 2: Wherein You Resist the Urge to Guess ###

Ask any programmer what the slowest portion of their system is and they'll likely mention a subsystem
with externally visible slowness. If you ask them _why_ it's slow, they'll be happy to tell you the 
exact portion of that subsystem's code responsible for the slowness.

    They're almost certainly wrong

There is a key truth to be mindful of while doing optimization work: _programmers are, as a rule, 
terrible at anticipating at the cause of slowness in their application._ This is counter-intuitive but almost always 
true. Time and time again developers will go off to "make something faster" without systematically _proving_ the 
cause of slowness and come back two weeks later with 700 lines of hand optimized code that have precisely __zero__ impact 
on overall performance. There's a good reason for this, although it's not an especially satisfying one: computers are complicated.
Even if you are aware of every cause of every performance issue ever, you'll still have an extremely difficult time anticipating
the cause of slowness through reasoning alone. The interaction between the different subsystems, logical units within those subsystems,
the operating system, the hardware, etc is just too complicated to be able to work out in your head. If it wasn't, we would never
have performance issues or, more tellingly, bugs in our software.

#### Families of Tools ####

Luckily, you don't have to rely on intuition when optimizing. There are scores of tools, both open and closed source, designed
to help developers find the reasons for a program's slowness. They can generally be divided into a few classes of tools:

##### Function Call Profilers #####

Profilers are tools that create an _execution profile_ of a running program. There are two general types of profilers: _statistical profilers_ and _instrumenting profilers_. Statistical profilers are typically added in at link time and take 'snapshots' of the executing program. These snapshots record the call stack of each thread of execution. Over time, the aggregate of these snapshots create a reasonably complete picture of the relative frequency of various operations (i.e. function calls). The other type of profiler interposes itself in some manner and records _every_ function call instead of a sampling. This higher level of detail comes at a cost: your program will typically run __noticeably__ slower while being profiled.

##### Cache profilers #####

Cache profilers are used to determine the memory access patterns of a program and how effective it is at utilizing the CPU's data cache. For each memory reference, the profiler will determine if the value was cached and at what cache level it was retrieved from. It also records cache misses, where the data must be retrieved from main memory.
 
Cache profilers are also usually capable of profiling instruction cache access as well. Similar to data cache, profilers typically record the count and source of cache hits and misses, as well as the cache level (if any) that eventually was found to contain the item in question.

Lastly, a number of cache profilers are able to profile _branch mispredictions_. When the CPU encounters a conditional branch in your code, like an if statement, it makes an (hopefully) informed guess as to which condition is more likely to be true. It can than prefetch the instructions for that branch of execution (or, depending on the architectures, multiple branches). In doing so, it avoids the need to wait until the CPU actually executes the conditional statement to fetch more instructions. Since CPU's use _pipelining_ to increase instruction throughput, waiting to see which conditional branch must be executed has a knock-on effect on subsequent instructions. If the CPU finishes executing a conditional instruction but the next instruction is not available (perhaps because the wrong branch was predicted), it must wait for the next set of instructions to be fetched, known as a _CPU stall_. 

##### Heap profilers #####

Inevitably in your optimization journey you'll come to realize a simple fact: dynamic allocation is _slow_. Really slow. You'll look at the profile output for a program and see all of the time being spent in '''malloc''' and '''free''' Enter heap profilers. Rather than telling you how much _time_ a portion of your code is taking, a heap profiler will tell you how much memory that portion is allocating. Many times, especially in enterprise development (for a reason I still don't really understand), objects are allocated on the heap, used as local variables, and destroyed without passing ownership elsewhere. This is both unnecessary and wasteful. Stack objects are created statically and accessed via an offset from the stack pointer. Using them is as close to "free" as you're going to get. Heap allocations are another thing altogether. You need to fetch a portion of memory from the OS which, as we discussed in describing cache profilers, is not always a lightening fast operation. Adding in virtual memory operations and the overhead of system calls in general and you've got one _slow_ operation for zero benefit. Also, physical memory is a shared resource, so you better be sure you free it lest you create a memory leak and slow down or crash the machine.

#### List of Profilers ####

Below are links to some profilers for Linux systems. The valgrind suite is usually my go-to set of profiling tools. That said, I've
personally used almost every tool on the list. All are helpful in some way.

1. [Valgrind](http://www.valgrind.org)
1. oprofile: part of the Linux kernel. Check your distro to determine how to install.
1. [VTune](http://software.intel.com/en-us/articles/intel-vtune-amplifier-xe/), Intel's profiler for Intel CPUs
1. [CodAnalyst](http://developer.amd.com/tools/CodeAnalyst/Pages/default.aspx) AMD's profiler for AMD CPUs
1. [gprof](http://en.wikipedia.org/wiki/Gprof) The GNU profiler, part of GNU binutils
1. [Google PerfTools](http://code.google.com/p/gperftools/) Now maintained outside of Google and renamed 'gperftools'.

_This brings us to the end of Part 1 of the series. Part 2 gets into the meat of how to approach software optimization. Look for 
here it next week._
