# Optimizing Django Views With C++


In my [previous post](http://www.jeffknupp.com/blog/2012/02/14/profiling-django-applications/) I outlined the method by which one goes about profiling a Django application. I used a view from [linkrdr](http://www.linkrdr.com) as an example. That view is responsible of aggregating, ranking, and sorting all of the links in a user's feeds (RSS, atom, Twitter, etc). The code from the post was an early, simplistic implementation of the view. I have, however, a much more robust scoring algorithm, written in Python, which I planned to used on the site.

You may have caught the word 'planned' in there. The algorithm turned out to be too slow. Rather, my Python implementation of the algorithm
was slower than what I deemed acceptable. After thinking of various architectural changes that could be made to solve the problem, I settled on a somewhat radical solution for a Django developer: __I implemented the view in C++__.

I realize that not every Django developer knows C++, nor should they, but those that do should realize it's a viable tool available when Python is just too slow. Eventually, you may get to a point where you can't really optimize your Python code any more. In this case, profiling will show that most of your time is spent in Python library calls. Once you hit that point, you've either written a horribly inefficient algorithm or you've got a problem not suited for Python.

When I realized I had hit that point with my view code, I panicked.
_'What more is there to do?'_ I wondered. Then I remembered a work
project where I had written some C++ code that interfaced with Python.
From a technical perspective, there was nothing stopping me from
implementing some aspects of my Django app in C++ (besides the fact
that it's _excruciating_ to write in coming from Python). Since linkrdr
is a single-person project, there are no teammates who need to grok the
code. I'm free to implement it as I wish.

<!--more-->
Setting Up
----------------

Having written "pure" C++/Python interoperability code before, and not
wanting to see `Py_XDecRef` again, I decided I would use boost::python. To begin, I made sure I had the latest [Boost](http://www.boost.org)
libraries and a recent version of gcc installed so I could use C++11
features, which really are rather nice. After building the newest
version of the boost::python library, I set out to learn how to actually
use the thing. It turned out to be incredibly easy.

boost::python wraps a number of Python data types for you: `object`
represents a generic Python object, `list` is a list, and so on. Since
Python is dynamically typed, there really aren't a whole lot of these.
'Everything is an Object' means that everything is a
boost::python::object and can be accessed in that way.

In addition to primitive and container type wrappers, boost provides a
clear and concise mechanism to make C++ classes and functions visible to Python. I had
a simple class in the code of my previous entry name `LinkScore`. It
was basically a C struct with a list of objects and an integer. The C++
code for it is:

    #!cpp
    using namespace boost::python;

    class LinkScore
    {
        public:
            LinkScore() {}
            LinkScore(const object& link, int score) : score_(score)
        {
            links_.append(link);
        }
        list links_;
        int score_;
    };

If you're thinking my data members should be private, guess what: I
don't care. That's part of the joy of working on code that only you will
use. You get to write it and use it however you want. 

The Details
----------------

Anyway, the boost::python code to make this callable from Python is:
    #!cpp
    class_<LinkScore>("LinkScore", init<object, int>())
        .def_readwrite("links", &LinkScore::links_)
        .def_readwrite("score", &LinkScore::score_);

Really, it couldn't be more simple. The `<Python.h>` way of
accomplishing this involves setting a struct with like 40 values to
declare each class. I was happy to not have to bother with that.

The actual code for my view is a free function called `get_scores`.
Here's a brief snippet:

    #!cpp
    using namespace boost::python;
    using namespace std;

    class CompareObject {
        public:
        bool  operator()(const LinkScore& l, const LinkScore& r) { return l.score_ > r.score_; }
    };

    list get_scores(object links)
    {
        object utility = import("links.utility");
        set<LinkScore, CompareObject> seen_links;
        list python_seen_links;
        for (int i = 0; i < len(links); ++i)
        {
            const object& link = links[i];
            LinkScore score = LinkScore(link, score_link (link, links));
            auto iter = seen_links.find(score);

            if (iter != seen_links.end())
            {
                // Do stuff
            }
            else
            {
                // Do other stuff
            }
        }
        // TODO: Optimize this
        for (auto i = seen_links.begin(); i != seen_links.end(); ++i)
        {
            python_seen_links.append(*i);
        }
        return python_seen_links;
    }

If you know C++ and Python, it's almost like reading a mix of the two.
The above, however, is valid C++ code and is the interface that Python
uses to call into my scoring library. To expose this function to Python,
all that's needed is `def ("get_score", get_score);` within a
`BOOST_PYTHON_MODULE` block, which names the module to be imported.

When I was done writing the C++ code, I compiled it using gcc and Boost's bjam build tool,
set my LD_LIBRARY_PATH to pickup libboost_python.so, and fired up a
shell from manage.py (well, a 'shell_plus' really). I used the cProfile
module to compare the C++ version of the view with the Python version of
the view. The results were satisfying: an 8x speedup with the C++
version. 

To call the C++ code, I just needed to make sure the .so generated was
on my PYTHON_PATH. I could then `import` it like a normal Python
library. I added it to my views.py and ran my unit tests. After they
passed, I committed everything and put the new code through it's paces
on the development web server. The response time was noticeably improved,
with the view being served seemingly instantaneously.

Wrap Up
-----------------

I realize this is not an optimization option available to everyone, but
it _is_ an option. Python is a fantastic language and Django is a nice
framework. When you need raw speed for computationally expensive
procedures, though, nothing beats getting closer to the metal. Overall,
I'm quite happy with the results and how easy it was to implement. I
will refrain from writing any more C++ code for linkrdr unless
absolutely necessary. It's nice to know, however, that the option is there.

Questions or comments on _Optimizing Django Views With C++_ ? Let me know in the comments below. Also, [follow me on Twitter](http://www.twitter.com/jeffknupp/) to see all of my blog posts and updates.
