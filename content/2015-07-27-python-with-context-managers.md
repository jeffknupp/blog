title: Python `with` Context Managers
date: 2015-07-27 19:07
categories: python with contextmanager

One commonly used Python language construct on which there is surprisingly
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
*runtime context*) is a block of code for which the user can declare an  
