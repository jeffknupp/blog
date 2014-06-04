Title: Python Deep Dive: Write an Interpreter in Python
Date: 2013-12-23 08:21
Category: Python
Tags: stuff
Slug: 2013-12-23-python-deep-dive-write-an-interpreter-in-python
Author: Jeff KNupp
Summary: short summary about my post


My "Improve Your Python" series focuses on explaining advanced Python
concepts to novice and intermediate Python programmers. This article,
however, is the first in a new series: *Python Deep Dive*. In *Deep Dive*
articles, I'll explore Python at a fundamentals level 
(occasionally down to the C code that implements it) in an effort to gain a more complete
understanding of how Python works "under the hood." In this article, we'll build
our own interpreter that mimics the operation of the cPython interpreter.

## The cPython Interpreter

It's important to remember *how* we actually run Python code: the cPython interpreter.
The *interpreter* is well-named; it *interprets* and executes Python code that you write.
But what does it mean to say that it *interprets* your code? 

To answer that we need to understand some basic terminology and concepts related
to writing interpreters in general. Ruby, Javascript, Python; all share a common series of 
operations at a high level:

* Lexing
* Parsing
* Execution

To build our parser, written in Python, we begin with *lexing*.

## Syntax

When the cPython interpreter opens a file, the first order of business is to
read the code contained in the file and make sense of it. To do so, the language
must have a well defined *syntax*. A language's syntax describes what words have
special meaning in the language and what combinations of those words and others 
are legal. For example, in Python `for <identifier> in <identifier>` is a legal
language construct. `for` and `in` are *reserved words* (those words with special
meaning I mentioned). 

So now we know our language needs a syntax, basically describing how you write
code in the language. Let's settle on the following:

### Assignment

Assignment will be done using `:=`, so the following is legal:

    #!go

    x := 10
    y := 'foo'

### Literals

A literal is a value found on the right hand side of the equal sign that is
*not* a variable. For example, in `x := 10`, `10` is an *integer literal*. 
In `y := 'foo'`, `foo` is a *string literal*. We'll allow for both integer
literals and string literals in our language.

### Looping

To keep things simple, we'll only support `while` for looping. Why does this
keep things simple? If we supported C-style `for` loops, we'd need to support
assignment, conditionals, and evaluation all in one statement. By restricting
looping to `while` loops, we only need to evaluate the `while` condition each
time through the loop. Loop bodies (and eventually function definitions) will 
be terminated by `end`. Rather than using braces (C-style) or 
indentation (Python-style), we'll again keep things simple by having a special
word that terminates loop constructs.

## Writing Some Code

Let's write the code 

it does so by looking
at each "word" in the file and identifying what type of "token" it is. The 
