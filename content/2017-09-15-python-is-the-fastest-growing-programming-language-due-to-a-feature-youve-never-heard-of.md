title: Python is the fastest growing programming language due to a feature you've never heard of
date: 2017-09-15 06:28
categories: python pandas numpy datascience

According to [a recent StackOverflow analysis](https://stackoverflow.blog/2017/09/06/incredible-growth-python/)
Python is the fastest growing programming language of those already in wide use. What's more, the growth rate is
*accelerating*, and has been consistently for the past few years. While the specific conclusions of the StackOverflow
post should probably be taken with a grain of salt, there's no denying the fact that Python use has exploded over the
past five years. That's great news for people who have long used and enjoyed the language, but it's still important to
ask *why* Python usage has exploded. And the primary, if not *sole* facilitator of this growth is a feature of the
language you've probably *never even heard of*.

## Big Data And The Reluctant Programmer

With the rise of Big Data, most industries found themselves in a scary situation: they had spent an enormous amount of
time and money building out their Big Data pipeline, but they were seeing little return on their investment. In the
breathless race to be able to capture ever-increasing volumes of data, most companies had no firm plan for what to *do*
with the data they captured. At the time, everyone thought that by storing huge amounts of data, analysis would be
simple and valuable business insights would almost be self-apparent. It may sound silly today, but most thought that
the patterns in the data would become obvious once enough data was captured.

**Unfortunately, that's not what happened.**

Instead, the industry collectively realized, almost simultaneously, that the kinds of non-trivial insights they hoped to glean and
questions they hoped to answer required rigorous mathematical analysis and validation. SQL queries might uncover the most obvious
patterns and trends, but the really juicy stuff required an entirely different skill set. A skill set firmly
rooted in statistics and applied mathematics, which no one outside of academia seemed to posses. What's more, a person
charged with analyzing these enormous data sets would need not only a very strong math background, *they'd need to be able to write software as well*.

It should come as no surprise, then, that the title "Data Scientist" started appearing all over both job sites *and*
resumes, though it would be a few years until anyone would attempt to nail down what exactly a Data Scientist *did* with
any rigor. At the time, it was closer to shorthand for "a person competent in both statistical analysis and
programming."

## Ruby vs. Python On The Web

Rewind a bit further, before Big Data was a real "thing", and you would have seen a heated battle between Ruby and Python to 
become "the language of the web". Both proved well suited for developing web applications. Ruby's popularity was
intimately tied to the [Rails]() framework. Few would argue that most programmers who self-identified as "Ruby
programmers" around this time might as well have just said "Rails programmers". Python was already reasonably well
entrenched in academia and a handful of disparate industries. The closest Python equivalent to Rails was [Django]().
Despite being released slightly ahead of Rails, it seemed to lag in popularity by a wide margin.

Many felt that the languages were similar enough in expressiveness and approachability that one would ultimately "win"
the web. But there was a fundamental difference in the implications of such an idea: while Ruby's popularity was 
closely intertwined with that of Rails, Django represented a comparatively small percentage of an already vibrant Python ecosystem.
Ruby, it seemed, needed Rails to "beat" Python to guarantee its continued popularity. And in many ways it did.

It just turned out to be the case that the "web wars" mattered far less than anyone anticipated.

## The Oliphant In The Room

To understand why, we'll need to go all the way back to 2006, when [Travis Oliphant](https://en.wikipedia.org/wiki/Travis_Oliphant) was still an assistant professor
at BYU and not co-founder of [Anaconda (nee Continuum Analytics)](https://www.anaconda.com/), one of the most successful commercial data science platforms built entirely on Python.
A year prior, he started the [NumPy](http://www.numpy.org/) project loosely based on a previous scientific computing library, Numeric. He would eventually go on to be a founding contributor to SciPy and even served as director of the
PSF. But in 2006, he submitted (along with Carl Banks) [PEP 3118](https://www.python.org/dev/peps/pep-3118/), a revision to Python's **"Buffer Protocol"**.

# Python's Buffer Protocol: The #1 Reason Python Is The Fastest Growing Programming Language Today
 
The buffer protocol was (and still is) an extremely low-level API for direct manipulation of memory buffers by other libraries. These are buffers created and used by
the interpreter to store certain types of data (initially, primarily "array-like" structures where the type and size of data was
known ahead of time) in contiguous memory. 
 
The primary motivation for providing such an API is to *eliminate the need to copy data when only reading, clarify ownership semantics of the buffer, and to store the data in contiguous memory (even in the case of multi-dimensional data structures), where read access is extremely fast.* 
Those "other libraries" that would make use of the API would almost certainly be written in C and highly performance sensitive. 
The new protocol meant that if I create a NumPy array of ints, other libraries can *directly access the underlying memory buffer* rather than requiring indirection or, worse, copying of that data before it can be used.

And now to bring this extended trip down memory lane full-circle, a question: what type of programmer would greatly benefit from fast, zero-copy memory access to large amounts of data?

**Why, a Data Scientist of course.**

## How We Got Here From There

So now we see the whole picture: 

* Oliphant and Banks propose a revision of Python's buffer protocol to simplify the direct access of the underlying memory of certain data structures, driven by work on the fledgling NumPy project. 
* [PEP 3118](https://www.python.org/dev/peps/pep-3118/) is submitted, accepted, and implemented.
* By virtue of PEP 3118's implementation, Python has quietly become an incredibly compelling language on which to build numerical computing libraries given that C extensions can share and manipulate data with very little overhead
* Python and Ruby fight it out on the web, where most assume the "language war" would be won
* As magnetic storage device prices plummet, it becomes feasible to store enormous amounts of data for later analysis (even if it's not clear what that analysis might entail; better to just save the data since it has become cheap enough to do so)
* The need for a new breed of programmer emerges: one with a background in statistics and/or applied math and little prior programming experience
* **Data Scientists**, looking for a language that is both expressive *and* fast (with good numerical computing library support to boot) all settle on Python
* In a follow up post, David Robinson of Stack Overflow details ["Why Python"](https://stackoverflow.blog/2017/09/14/python-growing-quickly/), making a compelling case for Data Science being the primary driver
* Jeff finally writes the article detailing why Python popularity has skyrocketed in the past five years that has been banging around in his head since contributing to the [Arrow](https://arrow.apache.org) and [Parquet](https://parquet.apache.org) projects

## Where Do We Go From Here?

In the second part of this article, I'll explain what *I've* been up to, Python-wise, for the past few years and how it
directly ties into the story above and the rise of the Data Scientist.
