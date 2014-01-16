It is difficult to fully appreciate Python, or, indeed, any interpreted
language, without having a basic understanding of the interpreter. In this
article, we'll look under the hood of the Python interpreter to gain an
understanding of how the code you write actually gets executed.

# What's in a name

The cPython *interpreter* is so-named due to it's function: the interpretation
of Python programs. Interpreted languages form one-half of the programming
lanugage ecosystem. The other are inhabited by languages like C, where programs are
staticly *compiled*. This compiled code eventually becomes assembly code
specific to the processor which will ultimately run the program.

In compiled languages, the code is not needed after it is compiled. One can
simply use the output of the compiler directly; the code that generated it may
be discarded. In interpreted languages, however, the code is key. It is being 
dynamically interpreted as it runs, so the source files must be present. This is
why you'll typically only recieve libraries for system packages written in C but
source code will be included in tools written in Python or Ruby.

An analogy will help illustrate the difference between compiled code and
interpreted code. Imagine you own a food truck, the kind that litter the streets
of New York and have gotten surprisingly upscale. You decide that you'll serve
sandwhiches, and settle on three that you think are quite tasty. Since your menu
is set in advance, you're able to make entire sandwhiches in the morning and,
when customers arrive, simply hand them out. There's really no work to be done
in making the sandwhich for a customer.

Your rival also happens to own a food truck that serves sandwhiches. Instead of 
a fixed menu, however, she has a list of available sandwhich ingredients listed.
The customer is free to add whatever combination they want at the time of their
order. While your rival can do some basic preperation, she can't reach your
level of efficiency in terms of serving customers.

She does, however, offer a wide variety of options, which some people value very
highly. Then again, while you can handle the lunch rush without batting an eye,
she leaves money on the table by servicing her customers much more slowly.
Clearly, there are tradeoffs to both approaches.

In this scenario, you are the compiled language and your rival the interpreted
one. Compiled languages do not change at run time; all the "preperation" is done
during compile time. *Because* the program can't change dynamically at run time,
the compiler can aggressively optimize each program it sees. Interpreters, on
the other hand, are "building sandwhiches on the fly". There is a clear tradeoff
in execution speed, but the gains in expressiveness often outweigh speed
concerns.

# Of yaccs and bison
