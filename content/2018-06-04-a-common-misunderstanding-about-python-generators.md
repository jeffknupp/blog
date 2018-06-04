title: A Common Misunderstanding About Python Generators
date: 2018-06-04 18:26
categories: python yield generator

I received the following email a few days ago:

> Jeff,
> 
> It seems that you know about iterators.  Maybe you can explain some weird behavior.  If you run the code below you will find that the function is treated differently just because it has a 'yield' in it somewhere, even if it's completely unreachable.
> 
```py

def func():
    print("> Why doesn't this line print?")
    exit() # Within this function, nothing should matter after this point.  The program should exit
    yield "> The exit line above will exit ONLY if you comment out this line."

x = func()
print(x)

```
>

When I run the code, I get the following output from the `print()` call: `<generator object func at 0x10e968a50>`.

So what's going on here? Why *doesn't* that line in `func()` print? Even if `yield` is completely unreachable, it *seems* to affect the way the function executes.

<!--more-->

## How `yield` affects a function

To shed some light on why this behavior is occurring, let's review `yield`. Any function that includes the `yield` keyword is automatically converted to a *generator*. What it returns (the *generator*) is a *generator iterator*. Our print output is actually hinting at this:

`$ python yield.py` 
`<generator object func at 0x10e968a50>`

When `x = func()` is executed, *we are not actually executing any of the code within `func()`*. Rather, since `func()` is a *generator*, a *generator iterator* is returned. So while that may look like a function call, it's actually giving us the *generator iterator* we would use to generate values yielded by the *generator*.

So how do we actually "call" a *generator*? *By calling `next()` on a generator iterator*. In the code above, this would execute the "next" call to the *generator iterator* returned by `func()` and bound to `x`.

If we want to see that cryptic message actually printed out, simply change the last line of the code to `print(next(x))`.

Of course, calling `next()` over and over on something that's meant to be treated as an iterator is a bit cumbersome. Luckily, `for` loops support iteration over *generator iterators*. Imagine a toy generator implemented as follows:

```py

def one_to_ten():
    """Return the integers between one and ten, inclusive."""
    value = 1
    while value <= 10:
        yield value
        value += 1

```

We can call this in a for loop in the following way:

```py

for element in one_to_ten():
    print(element)

```

Of course, we could have more verbosely written:

```py

iterator = one_to_ten()
for element in iterator:
    print(element)

```

This is similar to what the original code did. It just never used `x` to actually execute the code in the *generator*.

## Summary

I hope that clears up some common questions about `yield` and `generators` in Python. For a more in-depth tutorial on the topic, check out [Improve Your Python: 'yield' and Generators Explained](https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/).
