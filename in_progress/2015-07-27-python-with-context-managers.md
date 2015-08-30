title: Python `with` Context Managers
date: 2015-08-23 19:07
categories: python with contextmanager

One commonly used Python language construct for which there is surprisingly
little information is the `context manager` (and, by association, the `with`
keyword). Consider that the canonical way to open a file for reading/writing
uses a context manager, e.g.: 

```
with open('foo.txt', 'r') as infile:
    for line in infile:
        print '> {}'.format(line)
```

You'd think there'd be more on the subject, but I was hard-pressed to find many
guides on context managers suitable for novice/intermediate Python programmers.

Let's change that.

## "Context"?

Part of the confusion surrounding context managers is likely due to their name.
What exactly is a context and what does it mean to manage one? It doesn't help
that the offical Python documentation only uses the word "context" when
describing context managers. Otherwise the word has no meaning in the language.

Luckily, the concept of a context is relatively straightforward. A *context* (or
*runtime context*) is simply a nested block that defines a new *scope*. Remember
from the article on [TODO](Python's execution model):

> In Python, when a name is bound to an object,
> that name is only usable within the name's `scope`. The `scope` of a name is
> determined by the `block` in which it was created. A `block` is just a "block"
> of Python code that is executed as a single unit. The three most common types of
> blocks are modules, class definitions, and the bodies of functions. So the
> `scope` of a name is the innermost `block` in which it's defined.

Contexts add a little extra flavor to the normal code block: they give the user
an opportunity to perform any setup or object creation that will only exist
within the block. Usually, anything set up for a context also needs to be torn
down, otherwise the setup code may leak outside the context 

Going back to our canonical file example, imagine we want to open a file in a
context that we will create. The file should only be usable within that code
block (context). If we don't include teardown code to *close* the file at the
end of the context, though, that file will remain open after the end of the
context. 

Therefore, context managers are typically used to control access to some
resource. We don't want to put the burden on the programmer to remember to close
the file after using it, especially if there are multiple `return` statements or
`Exceptions` that can be raised. We want to provide some cleanup code and be
*guaranteed* that it always gets called.

Back to the example. For the moment, ignore the `with` and just know that
`infile` is set to the opened file resulting from the `open('foo.txt', 'r')`
call. Note that, once we leave the `with` block, `infile` is no longer a valid
variable; we can't refer to it anymore.

```
with open('foo.txt', 'r') as infile:
    for line in infile:
        print '> {}'.format(line)
```


You'll notice there's no explicit `infile.close()` here. As it turns out,
`open()` is a *context manager*. That means that, along with the standard
`open()` code to open a file and return a handle to the stream, `__enter__()` and
`__exit__()` methods are also defined. 
