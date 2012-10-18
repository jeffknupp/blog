title: "Writing a Python Book... in Python"
date: 2012-10-18 07:03
categories: python book software
---

After a surprisingly positive reception to my post [Writing Idiomatic
Python](www.jeffknupp.com/blog/2012/10/04/writing-idiomatic-python/) I decided
to [write an e-book](http://www.jeffknupp.com/blog/2012/10/11/idiomatic-python-ebook-coming/). Having never done so before,
I had no prior experience to guide me in how one should go about doing this.
While I could have spent a week researching the topic, I decided *writing* was
actually more important and I could figure the rest out as I go. Throughout this
process, I've settled on an method for writing and *testing* the
book, which is written entirely *in Python* (I'll explain below). I've noticed a
number of interesting parallels to general project development in Python, hence
this post.

<!--more-->

The book follows the format of my [original blog post](www.jeffknupp.com/blog/2012/10/04/writing-idiomatic-python/).
It is devided into sections loosely based on the situation in which you would
use the idiom (e.g. 'Managing Resources', 'Control Structures', etc.). Each of
these sections is a Python module (possibly containing other modules). The top
level directory looks like this:

    jeff:~/code/idiom/|master -> l
    total 8
    drwxr-xr-x 9 jeff users 1024 Oct 17 12:47 working_with_data
    drwxr-xr-x 3 jeff users 1024 Oct 17 14:03 script_writing
    drwxr-xr-x 3 jeff users 1024 Oct 17 14:03 recipes
    drwxr-xr-x 3 jeff users 1024 Oct 17 17:40 managing_resources
    drwxr-xr-x 3 jeff users 1024 Oct 17 17:42 functions
    drwxr-xr-x 5 jeff users 1024 Oct 17 17:44 control_structures
    drwxr-xr-x 3 jeff users 1024 Oct 17 17:48 formatting
    -rw-r--r-- 1 jeff users  129 Oct 17 17:48 Makefile

Within each module are Python individual idioms, each written as a Python
script. For example, here is the complete file representing the idiom "Avoid 
repeatedly checking a variable's value in a compound if statement":

    ```py
    """
    ####Avoid repeatedly checking a variable's value in a compound if statement
    When one wants to check against a number of values, repeatedly listing the variable whose value is being checked is unnecessarily verbose. Using a temporary collection makes the intention clear.
    """
    from nose.tools.trivial import assert_true
    name = 'Tom'

    def run_asserts(local_dict, global_dict):
        assert_true(local_dict.get('is_generic_name'))

    def test_idiomatic():
        is_generic_name = False
        if name in ('Tom', 'Dick', 'Harry'):
            is_generic_name = True

        run_asserts(locals(), globals())

    def test_harmful():
        is_generic_name = False
        name = 'Tom'
        if name == 'Tom' or name == 'Dick' or name == 'Harry':
            is_generic_name = True

        run_asserts(locals(), globals())

Obviously, simply concatenating these scripts and calling it a book would make 
for a very unreadable "book". Instead, the book proper is generated using a 
few simple tools (described below). For now, let's focus on the structure of the idiom.

As you can see, the idiom's text is stored in a [docstring](http://docs.python.org/dev/tutorial/controlflow.html#documentation-strings).
This keeps the text and code together, useful when making changes where both
will need to be updated. There's some Markdown in there, too. Just like on this
blog, I'm using Markdown to structure the text, mostly because I'm a)
comfortable with it and b) I know it can be translated to a variety of formats.

After the initial text, you'll notice some imports from the ```nose``` package.
[Nose](http://pypi.python.org/pypi/nose/1.2.1) is a package that extends
unittest while at the same adding a number of other useful features (including
support for doctests, capturing stdout during tests, test decorators, and about
a dozen other things). Using ```nose```, the file transforms from an odd way to
store sections of a book to a *fully testable artifact*. Until I hit upon this
structure, checking the code for each idiom worked as intended (and that the
'Harmful' and 'Idiomatic' code produced the same value) was a manual,
time-intensive task. Now, it takes 5 key presses to determine if all of the code
in all of the idioms are correct.

You may have noticed the function ```run_asserts``` in the code above, taking
two dictionaries as arguments. It's purpose is to ensure that
```test_idiomatic``` and ```test_harmful``` not only work as intended, but that
they test the same thing. If I had simply listed the asserts at the end of each
function, it wouldn't take long before I accidentally updated one set and not
the other. This way, I can be sure both functions work and produce the same
results.
