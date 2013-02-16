title: Writing a Python Book... in Python
date: 2012-10-18 07:03
categories: python book software


After a surprisingly positive reception to my post [Writing Idiomatic
Python](http://www.jeffknupp.com/blog/2012/10/04/writing-idiomatic-python/) I decided
to [write an e-book](http://www.jeffknupp.com/blog/2012/10/11/idiomatic-python-ebook-coming/) (if you'd like updates on the book's
progress, a sign up widget is available below). Having never done so before,
I had no prior experience to guide me in how one should go about doing this.
While I could have spent a week researching the topic, I decided *writing* was
actually more important and I could figure the rest out as I go. Throughout this
process, I've settled on an method for writing and *testing* the
book, which is written entirely *in Python* (I'll explain below). I've noticed a
number of interesting parallels to general project development in Python, hence
this post.

<!--more-->

##Intermezzo: Get updates on the progress of 'Writing Idiomatic Python'
If you'd like to receive updates on the progress of 'Writing Idiomatic Python',
sign up with your email address using the widget below. No spam. Promise.

<div rel="FUG7A5IM" class="lrdiscoverwidget" data-logo="on" data-background="off" data-share-url="jeffknupp.com/blog/2012/10/18/writing-a-python-book-in-python/" data-css=""></div><script type="text/javascript" src="http://launchrock-ignition.s3.amazonaws.com/ignition.1.1.js"></script>

##A book you can run from the command line...

The book follows the format of my [original blog post](http://www.jeffknupp.com/blog/2012/10/04/writing-idiomatic-python/).
It is divided into sections loosely based on the situation in which you would
use the idiom (e.g. 'Managing Resources', 'Control Structures', etc.). Each of
these sections is a Python module (possibly containing other modules). The top
level directory looks like this:

    :::bash
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

    #!python
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

##This book has a build process...

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
they test the same thing. It is called with the ```locals``` and ```globals```
of the test function, which represent the current scope's local and global
variables respectively. This gives me a consistent interface to call the
```run_asserts``` function. Each idiom contains a ```run_asserts``` that differ
only in the values they check. If I had simply listed the asserts at the end of each
function, it wouldn't take long before I accidentally updated one set and not
the other. This way, I can be sure both functions work and produce the same
results.

When I actually want to run the tests, I simply type ```make``` to invoke my
Makefile. Its contents are straightforward:

    #!Makefile
    all:
        PYTHONWARNINGS=all nosetests-3.4 -s --with-doctest --with-coverage --cover-erase --all-modules --doctest-options=+ELLIPSIS

There are some nose-specific options there, as well as setting the environment
variable ```PYTHONWARNINGS``` to "all", turning on warnings which alert
about unclosed files and the use of deprecated functions, among other things.
The output of ```make``` gives me a good deal of information:

    :::bash
    ...
    idiom.working_with_data.dictionaries                                                  0      0   100%   
    idiom.working_with_data.dictionaries.dict_get_default                                11      1    91%   19
    idiom.working_with_data.lists                                                         0      0   100%   
    idiom.working_with_data.lists.list_comprehensions                                    14      0   100%   
    idiom.working_with_data.lists.unpacking_rest                                          8      0   100%   
    idiom.working_with_data.strings                                                       0      0   100%   
    idiom.working_with_data.strings.chain_string_functions                               10      5    50%   21-25
    idiom.working_with_data.strings.string_join                                          11      0   100%   
    idiom.working_with_data.tuples                                                        0      0   100%   
    idiom.working_with_data.tuples.tuple_underscore                                      13      0   100%   
    idiom.working_with_data.tuples.tuples                                                10      0   100%   
    idiom.working_with_data.variables                                                     0      0   100%   
    idiom.working_with_data.variables.temporary_variables                                12      0   100%   
    ---------------------------------------------------------------------------------------------------------------
    TOTAL                                                                               317     16    95%   
    ----------------------------------------------------------------------
    Ran 70 tests in 0.306s

    OK

Here I can see both the status of my tests as well as the code coverage for each
idiom (looks like I have a bit of work to do...). 

This post has already become quite long, so I'll break here for now. Tomorrow,
I'll show how I process the idiom Python files to produce the actual book in 
a variety of formats.
