title: Don't Write Python Scripts, Write Python Libraries
date: 2014-04-03 17:42
categories: python

When someone asks why the `if __name__ == '__main__'` idiom should be used, I
say it's because it makes turning your "script" into a "library" a seamless
act. Novices often write a series of one-off Python scripts that exist only as
long as it takes to finish and run them. More seasoned developers have accumulated a set of *libraries* they've written over
the years.

Last night I needed to properly parse a fully-qualified domain into
its constituent parts (top-level domain, second-level domain, sub-domains). I
found one library that looked promising, but it used a hard-coded list to
represent all of the possible TLDs. The problem is this list changes with some 
frequency, and I needed to get it right. 

So, fine, there's no third-party package that exactly fits my needs. Rather than
just bolt on the domain parsing functionality to the application that required
it, however, I turned it into a first-class citizen: a library (more accurately,
a Python package). Heck, I even [released it](https://github.com/jeffknupp/domain-parser) with unit tests and hooked it up to
TravisCI.

Why would I take the extra time required to make this a reusable library? Two
main reasons: first, this is a straightforward problem that should be solved once and never
thought of again. Any time you encounter situations like that, do the right
thing and write a small library. Second, because it's a general enough task,
I wanted to make it available to others so that they didn't need to keep solving
a problem that's already been solved.

## Solved Problems

As developers, we waste *a ton* of time on solved problems. Whether it's due to
"Not Invented Here"-itis or general ignorance, I've seen entire systems
duplicated by different teams in the same organization. I would argue that being 
able to sense when a problem likely has an open source solution is an integral
part of being a "good" developer. 

So in the interest of saving everyone a bunch of time, I wrote the package, released it,
and am happy to accept bug reports (and will fix them). What's more, the library
becomes another tool in my tool belt rather than a few random functions in a
script I'll never use again. 

As developers, we should be working together
on the mundane stuff so that we can all go off and work on the cool stuff.
Please, don't make other people solve your problem over and over again. Do it
once, make a library, and release it to the world. You'll save all of us a lot
of time.
