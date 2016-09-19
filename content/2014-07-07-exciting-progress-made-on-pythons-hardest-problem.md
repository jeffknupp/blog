title: Exciting Progress Made on 'Python's Hardest Problem
date: 2014-07-07 21:46
categories: python gil pypy

A long awaited announcement was finally [made Saturday by the PyPy team](http://morepypy.blogspot.com/2014/07/pypy-stm-first-interesting-release.html): 
PyPy-STM has reached a reasonable level of maturity and usefulness to begin
comparison to PyPy and cPython. We can consider the first (C-based) GIL-less
Python (disregarding that old "no GIL" patch from years ago which went nowhere).
<!--more-->

The implications are important: Armin and team have proven that Software
Transactional Memory is a viable approach to GIL-less multi-threaded Python.
They are now ready to move to the second phase of the project, namely
improving things to the point that there are no caveats to the statement
"PyPy-TM can run existing multi-threaded Python code without a GIL and 
achieve reasonable speed-ups".

As someone who has followed GIL-related work for years (albeit from the
sidelines) I can't understate how excited I am. Though Python continues to enjoy a
reasonably high rate of adoption (I assume) across a number of disciplines, the
GIL always made taking full advantage of today's multi-core hardware difficult at
best. In a GIL-only world, Python may be discarded for similar languages that do
not share the same drawback, especially as they mature.

Today's announcement, however, has made clear a road ahead for Python. If Armin
and company are able to complete the second phase of the project (scheduled to
last up to two years), I can imagine a world where PyPy becomes the reference
implementation of Python. As crazy a statement as that sounds, that's how
important I believe solving this problem is.

In general terms, today's announcement was a win for developer ingenuity and
perseverance. Work on the STM branch began years ago, and there were a number
of false starts. The team kept at it, though, and showed the rest of us
that the hard problems *are* worth working on, assuming enough dedication (and not a little
bit of intelligence and skill!). It's a win for those operating on the fringes of
their fields, on the problem that few discuss and less try to solve. Most
importantly, it's a win for the Python community at large.

Good luck to Armin and Remi (who are both committed to phase two assuming there
is funding), as well as all who join them and contribute development time.
I, for one, [will be donating](http://pypy.org/tmdonate2.html) to support their worthy research.
