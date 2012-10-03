title: "Software Optimization: A Systematic Approach, Part Two"
date: 2012-10-02 12:42
categories: software optimization linux c++
---

*Note: I apologize for the radio silence over the past 3 months. I got married at
the end of July and between wedding related stuff and one other reasonably large
time sink (which I'll hopefully be able to share here soon), I've been quite busy. 
My intention going forward is to post a new portion of SO:ASA every two weeks (one week proved 
to be too sensitive to outliers in my schedule). I'm also going back through 
all of the comments from the past two months and responding or contacting 
the author as appropriate. Regardless, hope you enjoy this installment.*

-**Jeff**

#Part Two
*In case you missed it, [Part One is available here](http://www.jeffknupp.com/blog/2012/07/10/software-optimization-a-systematic-approach/).*

##The Case of the Idiot Detective##

Our end goal in optimization is not to merely increase performance. Rather, it is to do increase performance *with proof that our changes were responsible*. When you finish your optimization task, you'll likely face the same two questions from whomever you show the new code to: 

1. How much faster is it?
2. Why?

Your goal is to have hard data that answers those questions for you, and this forms the cornerstone of our approach. 

A natural analogy for optimization is detective work. Imagine yourself investigating a robbery at the mansion of your least-favorite wealthy celebrity: You arrive on the scene and are told that, among other things, a priceless piece of art was stolen. Without having even surveyed the scene or collected evidence, you shout out "Professional art theif!" and run back to the station to research every art theif you've ever heard of.

Hopefully, this sounds like a ridiculous way to investigate a crime. Unfortunately, it's the exact method employed by a large number of programmers when tasked with optimization. Instead of doing the appropriate investigation, they make an initial guess based on little more than gut-feeling and programming myths and rush off to fix a portion of the process that is quite likely not the culprit.

Instead, we'll be the dogged investigator who carefully analyzes the crime scene, collects potential evidence, and lets that evidence drive the investigation. When the case has been solved and we present our findings to the jury, the evidence will be damning and overwhelming. Remember, solving the case is not enough. *We need to be able to convince the jury that we actually caught the guilty party*.

##Introducing the S.M.A.R.T Methodology

In our approach to optimization, every step is motivated by data produced from the previous step. All of this data is saved, both to aid in our analysis and to help build the final report proving our changes improved performance.

To optimize software without guesswork and wasted effort, one has to be 
**SMART**. In keeping with this, I've named the methodology used for the 
rest of this paper is the **S.M.A.R.T** method. The goal is to never encounter a 
situtation where you do some work and then think, "OK, now what?". Data
tells us what to work on. The **S.M.A.R.T** method tells us *how* to work 
on it.

<!--more-->

###Components of the S.M.A.R.T Methodology

1. Sandbox
1. Measure
1. Analyze
1. Refactor
1. Test

In the sections below, I'll introduce each component in the **S.M.A.R.T**
methodology and explain its usefulness. In **Part Three**, I'll describe in detail 
the work to be done in each step.

##Sandbox
*Sandboxing*, in software development, refers to the creation of an environment
where untested code can run without affecting (or being affected by) processes
or data outside the sandbox. It is akin to a cleanroom in manufacturing or
research, which completely isolates the material being worked on from the
external environment. The rationale for creating such an environment for
software is much the same as for other fields: *to prevent external sources from
affecting the sandboxed system*.

####Based on a True Story
To see why sandboxing is critical, consider the following example from a project
I worked on:
    
> A coworker was testing the effects of a series of optimizations he had
> applied to our system (a high-throughput transaction processing system).
> The tests results were highly favorable, with one exception: While the
> mean transaction took around 500us, the first transaction in a long series 
> took five to six times that long. It was easily repeatable but had no obvious
> cause. There was no data to be precomputed or caches to warm. The first
> transaction was processed in exactly the same way as every other transaction.
> 
> When I asked him where he was testing, his answer surprised me. He was testing
> on one of our development servers, the configuration of which was vastly
> different from our production servers. After giving it a few minutes of
> thought, I pointed him to the likely culprit: CPU frequency scaling. Used to
> conserve power when a machine is under light load, Linux has the ability to
> dynamically change the frequency of the system's CPUs. When load increases,
> the frequency can be similarly increased. This would manifest itself in
> exactly the way he was seeing: A portion of the initial work would be slower
> than normal, but this would change quickly and the remaining work would be
> completed in the expected amount of time.

The reason this never occurred to him as the cause of slowness was simple: *Our
production servers were set up differently*. For obvious reasons, frequency scaling was
configured to be turned off in production. **Because he had failed to isolate
his test environment, his test results were silently being affected.** How could
he have prevented this? Simple. By running his tests on a machine
configured identically to our production machines. Sandboxing, in the context of
optimization, is not only about insulating your process from the effects of other 
processes on the machine. Sandboxing requires insulating your process *from the
machine itself*.

####Sandboxes in Sandboxes
While mostly used in terms of complete processes or systems, Sandboxing can
refer to a component *within* a system. When we want to isolate a portion of
code for testing purposes, we create a virtual sandbox through the use of common
unit testing idioms like mocking. **The goal of sandboxing is to never wonder if 
your test results reflect anything other than the code you meant to test.**

##Measure
Perhaps the most important step in the **S.M.A.R.T** methodology is the second:
Measure. It refers to measuring program execution through the use of a profiler.
Without measuring, we are forced to resort to guesswork and intuition. As
mentioned earlier, when it comes to optimization, guesswork and intuition are
two areas in which all programmers are spectacularly bad.

####Consistent, Automated, Repeatable
To be useful, profiling must be done in a consistent, automated, repeatable way.
Be it through the use of a few shell scripts or an expensive, third-party tool,
beginning a profile 'run' should take a single command or button press. If there
is configuration, it should match the production configuration as closely as
possible. The duration of a profiling run should be the minimum amount of time
the process needs to produce useful profiling output. This will vary between systems, 
but you should invest a bit of effort up front to minimize this time. 
No one likes staring at a screen waiting for a test to finish.

####Record Keeping
Profiling data should be saved after each run, ideally directly in your version
control system. In this way, you can see the effect of your changes on
performance over time. Remember, our goal is to *prove* our changes
directly resulted in the performance gains we report. Without saving the output
of each profiling runs, we have no way of determining the effect of individual 
changes.

####Presenting Data
When presenting profiling data as part of a report, one needs to be sure that
the numbers and units used are meaningful. For example, *callgrind* has an
option to show the cost of function calls as either a percentage of the
program's total execution or as the number of instructions executed. While the
former is useful to quickly identify hotspots it is effectively useless out of
context. If you have optimized a portion of your program, subsequent runs will
show untouched code costing a higher percentage than before simply because the
overall number of instructions executed has been reduced. By showing values in 
an absolute scale, we are able to immediately compare two different runs and 
discern what changed (and by how much).
