# The Writing Idiomatic Python Book is Finally Available!

It took far more effort and time than I ever anticipated, but the [Writing Idiomatic Python eBook](http://www.jeffknupp.com/writing-idiomatic-python-ebook/)
is finally available! It's in "beta" mode right now, meaning I'm still planning
on adding more content over the next month, but if you get it today you'll
automatically get all of the updates (and corrections) for free. I really
believe that the book will be of use to both those new to Python and those
looking to increase their Python mastery.

# Behind the scenes

Interestingly, the book has its own automated build and test process, and it's
the most comprehensive I've ever used on a Python project. As the book is
primarily comprised of code samples, regression testing is an absolute must. I'm
using [pytest](http://pytest.org/latest/) to implement the tests themselves. I
found it a bit more flexible than nose in terms of deciding which 
directories/files/functions should be searched for tests. I'm also using
the `coverage` package to make sure all of the code samples are actually being
tested properly.
<!--more-->
Since there are two different versions of the book (one for Python 2.7.3+ 
and one for Python 3.3+), [tox](http://tox.readthedocs.org/en/latest/) is used 
to test each version of Python against the non-version specific tests plus 
those specific to version of Python being used. tox is incredibly flexible, 
which has been vital as my "project" is much different than most other Python
projects.

## Building the book

After the tests complete, a custom Python `generate` script traverses each
directory and process the .py files it finds. Section headings are stored in
`__init__.py` files, while individual idioms are normal Python files. For each
idiom, the file's docstring represents the idiom's description and analysis (
written in Markdown). This is followed by two functions: `test_harmful` and 
`test_idiomatic`, which contain the actual sample code. 

The `generate` script extracts the code from the two functions just mentioned
as code objects and does a bit of post-processing (stripping out doctest related
docstrings and pytest assertions). The sample code often uses non-existent
functions and classes for illustrative purposes, but these need to exist in
order to test the samples. "Helper" code implements the non-existent classes and
functions in such a way that the sample code both runs and gives sensible
values. The helper code for each idiom resides in that idiom's file and is
stripped out by the `generate` script.

## An example idiom

To make the above a bit more clear, here's the full text of a sample file for a
single idiom (in this case named `use_else_to_determine_when_break_not_hit.py`):

    #!py
    """
    Use ``else`` to execute code after a ``for`` loop concludes
    One of the lesser known facts about Python's ``for`` loop is that it can
    include an ``else`` clause.  The ``else`` clause is executed after the
    iterator is exhausted, unless the loop was ended prematurely
    due to a ``break`` statement. This allows you to check for
    a condition in a ``for`` loop, ``break`` if the condition holds for an
    element, ``else`` take some action if the condition did not hold for
    any of the elements being looped over. This obviates the need for conditional
    flags in a loop solely used to determine if some condition held.

    In the scenario below, we are running a report to check if any
    of the email addresses our users registered are malformed
    (users can register multiple addresses). The idiomatic
    version is more concise thanks to not having to deal
    with the `has_malformed_email_address` flag. What's more,
    *even if another programmer wasn't familiar with the `for ... else` idiom, our code is clear enough to teach them.*
    """



    class User():
        def __init__(self, name, email_list):
            self.name = name
            self.email = email_list

        def get_all_email_addresses(self):
            return self.email

        def __str__(self):
            return self.name


    def get_all_users():
        return [User('Larry', ['larry@gmail.com']),
                User('Moe', ['moe@gmail.com', 'larry@badmail.net']),
                User('Curly', ['curly@gmail.com'])]

    def email_is_malformed(email_address):
        return 'badmail' in email_address

    def test_idiomatic():
        """
        >>> test_idiomatic()
        Checking Larry
        All email addresses are valid!
        Checking Moe
        Has a malformed email address!
        Checking Curly
        All email addresses are valid!
        """
        for user in get_all_users():
            print ('Checking {}'.format(user))
            for email_address in user.get_all_email_addresses():
                if email_is_malformed(email_address):
                    print ('Has a malformed email address!')
                    break
            else:
                print ('All email addresses are valid!')

    def test_harmful():
        """
        >>> test_harmful()
        Checking Larry
        All email addresses are valid!
        Checking Moe
        Has a malformed email address!
        Checking Curly
        All email addresses are valid!
        """
        for user in get_all_users():
            has_malformed_email_address = False
            print ('Checking {}'.format(user))
            for email_address in user.get_all_email_addresses():
                if email_is_malformed(email_address):
                    has_malformed_email_address = True
                    print ('Has a malformed email address!')
                    break
            if not has_malformed_email_address:
                print ('All email addresses are valid!')

You may notice in the description that some terms are surrounded by a single \` and others
by two. This is used for the purposes of building the index at the end of the
book. Anything with two \`'s is both formatted as inline code and marked as an
occurrence of that term for the index. A single \' is similarly formatted but not
indexed (so useless phrases like `has_malformed_email_address` don't appear in
the index). The `generate` script takes the appropriate action based on which
style of backquote is used.

So after all of these steps are completed, the generate script produces a single
Markdown file that represents the complete text of the book, properly formatted.
This is then run through [pandoc](http://johnmacfarlane.net/pandoc/) with a
custom latex template to produce a '.latex' file. This gets run through
`xelatex` so that the index may be generated, `makeindex` is used to 
actually build the index, and `xelatex` is run again to produce the 
final PDF document.

## In retrospect...

Of course, none of this infrastructure existed when I started. I had no idea how
I was going to write the prose and test the code at the same time. I had no idea 
how PDF files could be created. I had never used latex in any form. All of the
above just gradually grew out of necessity. Looking at it all now, I'm amazed I
had the patience to set it all up since *none of it is evident in the final
product (the book)*.

You can imagine, then, the pace at which the book has been written. I have a
full time job, so work was done in hours stolen from evenings and weekends. My
wife has been more supportive of this than I deserve, but is glad that it's
quite close to ending. I have a new found respect for those that write technical
books for a living. It is a mentally and emotionally draining process.

In the end, though, all that matters is the following: I set out to write a book
that newcomers to Python would find helpful, I worked on it whenever I could,
and *I actually finished it*. The last part is the key. I have started and
abandoned scores of projects, as I'm sure many of you have. This time, though,
I persevered. This time I finished. Even if no one actually buys the [book](http://www.jeffknupp.com/writing-idiomatic-python-ebook/), I still got through the process of writing it.

That's worth quite a lot to me.
