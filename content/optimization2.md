#Part 2#

##The Case of the Idiot Detective##

Our end goal in optimization is not to merely increase performance. Rather, it is to do increase performance *with proof that our changes were responsible*. When you finish the task, you'll likely face the same two questions from whomever you show the new code to: 

1. "How much faster is it?"
2. "Why?"

Your goal is to have hard data that answers those questions for you, and this forms the cornerstone of our approach. 

A natural analogy for optimization is detective work. Imagine yourself investigating a robbery at the mansion of your least-favorite wealthy celebrity: You arrive on the scene and are told that, among other things, a priceless piece of art was stolen. Without having even surved the scene or collected evidence, you shout out "Professional art theif!" and run back to the station to research every art theif you've ever heard of.

Hopefully, this sounds like a ridiculous way to investigate the crime. Unfortunately, it's the exact method employed by a large number of programmers when tasked with optimization. Instead of doing the appropriate investigation, they make an initial guess based on little more than gut-feeling and programming myths and rush off to fix a portion of the process that is quite likely not the culprit.

Instead, we'll be the dogged investigator who carefully analyzes the crime scene, collects potential evidence, and lets that evidence drive the investigation. When the case has been solved and we present our findings to the jury, the evidence will be damning and overwhelming. Remember, solving the case is not enough. *We need to be able to convince the jury that we actually caught the guilty party*.

##The Data Driven Approach##

In our approach to optimization, every step is motivated by data produced from the previous step. All of this data is saved, both to aid in our analysis and to help build the final report proving our changes improved performance.

We will follow a simple, iterative, four-step process:

* **Isolate**- Create an isolated, repeatable environment in which to run our tests.
* **Profile**- Run our tests with the aid of a profiler to generate a *test profile*.
* **Analyze**- Inspect our profiling results and identify the largest contributor to poor performance
* **Optimize**- Optimize the under-performing code using straightforward techniques.

We simply repeat these steps, feeding in the results of our last round, until we have acheived the desired performance.



##Setting up your cleanroom##

