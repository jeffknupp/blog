title: Writing Python Functions That Don't Suck
date: 2015-08-27 18:36
categories: python function iyp

Functions are one of the fundamental building blocks of *most* programming
languages. They are the simplest form of abstraction, the concept upon which
modern programming is built. 

**So you better know how to write them well.**

What differentiates a "good" Python function from a crappy one? You'd be
surprised at how many definitions of "good" one can use. For our purposes, I'll
consider a Python function "good" if it can tick off the items on this
checklist: 

* Has a single responsibility
* Sensibly named
* Includes a docstring
* Returns a value
* Is *idempotent*
* Is no longer than 50 lines

For many of you, this list may seem overly draconian. I promise you, though, if
your functions follow these rules, your code will be so beautiful it will make
unicorns weep.

Below, I'll devote a section to each of the items, then wrap things up with how
they work in harmony to create "good" functions.

## Has a single responsibility

A function should do one, and only one, thing. Calculate 
