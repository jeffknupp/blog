title: Starting A Python Project The Right Way
date: 2014-02-04 09:00
categories: python virtualenv git

If you're like most novice Python programmers, you likely are able to envision
entire applications in your head but, when it comes time to begin writing code
and a blank editor window is staring you in the face, you feel lost and
overwhelmed. In today's article, I'll discuss the method *I* use to get myself
started when beginning a program from scratch. By the end of the article, you
should have a good plan of attack for starting development for any application.
<!--more-->
## Setup

Before a line of code is ever written, the first thing I do is create a *virtual environment*.
What is a virtual environment? It's a Python installation completely segregated
from the rest of the system (and the system's default Python installation). Why
is this useful? Imagine you have two projects you work on locally. If both use
the same library (like `requests`) but the first uses an older version (and
can't upgrade due to *other* libraries depending on the old version of
`requests`), how do you manage to use the newest version of `requests` in your
new project? The answer is virtual environments.

To get started, install `virtualenvwrapper` (a wrapper around the fantastic
`virtualenv` package). Add a line to your .bashrc or equivalent file to source
/usr/local/bin/virtualenvwrapper.sh and reload your profile by `source`ing the 
file you just edited. You should now have a command, `mkvirtualenv`, available
via tab-completion. If you're using Python 3.3+, virtual environments are
supported by the language, so no package installation is required. `mkvirtualenv <my_project>` will
create a new virtualenv named `my_project`, complete with `pip` and `setuptools`
already installed (for Python 3, `python -m venv <my_project>` followed by
`source <my_project>/bin/activate` will do the trick).

Now that you've got your virtual environment set up, it's time to initialize
your source control tool of choice. Assuming it's `git` (because, come on...),
that means `git init .`. It's also helpful to add a `.gitignore` file right away
to ignore compiled Python files and `__pycache__` directories. To do so, create
a file named `.gitignore` with the following contents:

    *.pyc
    __pycache__

Now is also a good time to add a `README` to the project. Even if you are the only
person who will ever see the code, it's a good exercise to organize your
thoughts. The `README` should describe what the project does, its requirements,
and how to use it. I write `README`s in Markdown, both because GitHub
auto-formats any file named `README.md` and because I write **all** documents in
Markdown.

Lastly, create your first commit containing the two files (`.gitignore`,
`README.md`) you just created. Do so via `git add .gitignore README.md`, 
then `git commit -m "initial commit"`.

## SKELETONS!

I begin almost every application the same way: by creating a "skeleton" for the
application consisting of functions and classes with docstrings but no
implementation. I find that, when forced to write a docstring for a function I
*think* I'm going to need, if I can't write a concise one I haven't thought
enough about the problem.

To serve as an example application, I'll use a script recently created by a
tutoring client during one of our sessions. The goal of the script is to 
create a csv file containing the top grossing movies of last year (from IMDB) and the 
keywords on IMDB associated with them. This was a simple enough project that it
could be completed in one session, but meaty enough to require some thought.

First, create a main file to serve as the entry point to your application. I'll
call mine `imdb.py`. Next, copy-and-paste the following code into your editor
(and change the docstring as appropriate):

    #!py
    """Script to gather IMDB keywords from 2013's top grossing movies."""
    import sys

    def main():
        """Main entry point for the script."""
        pass

    if __name__ == '__main__':
        sys.exit(main())

While it may not look like much, this is a fully functional Python program. You
can run it directly and get back the proper return code (`0`, though to be
fair, running an empty file will also return the proper code). Next I'll create
stubs for the functions and/or classes that I think I'll need:

    #!py
    """Script to gather IMDB keywords from 2013's top grossing movies."""
    import sys

    URL = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us,desc&start=1&year=2013,2013"

    def main():
        """Main entry point for the script."""
        pass

    def get_top_grossing_movie_links(url):
        """Return a list of tuples containing the top grossing movies of 2013 and link to their IMDB
        page."""
        pass

    def get_keywords_for_movie(url):
        """Return a list of keywords associated with *movie*."""
        pass

    if __name__ == '__main__':
        sys.exit(main())  

That seems reasonable. Notice that the functions both include parameters (i.e.
`get_keywords_for_movie`, includes the parameter `movie_url`). This may seem 
odd when implementing stubs. Why include any parameters at this point? The 
reasoning is the same as for pre-writing the docstring: if I don't know what 
arguments the function will take, I haven't thought it through enough.

At this point, I'd probably commit to `git`, as I've done
a bit of work that I wouldn't like to lose. After that's done, it's on to the
implementation. I always begin implementing `main`, as it's the "hub" connecting
all other functions. Here's the implementation for `main` in `imdb.py`:

    #!py
    import csv

    def main():
        """Main entry point for the script."""
        movies = get_top_grossing_movie_links(URL)
        with open('output.csv', 'w') as output:
            csvwriter = csv.writer(output)
            for title, url in movies:
                keywords = get_keywords_for_movie(
                    'http://www.imdb.com{}keywords/'.format(url))
                csvwriter.writerow([title, keywords])

Despite the fact that `get_top_grossing_movie_links` and `get_keywords_for_movie` 
haven't been implemented yet, I know enough about them to make use of them.
`main` does exactly what we discussed in the beginning: gets the top grossing
movies and outputs a csv file of their keywords.

Now all that remains is the implementation of the missing functions.
Interestingly enough, *even though we know `get_keywords_for_movie` will be called **after** `get_top_grossing_movie_links`, we can implement them in whatever order we like.*
This isn't the case if you simply started writing the script from scratch,
adding things as you go. You would be forced to write the first function before
you could move on to the second. The fact that we can implement (and test!) the
functions in any order shows they are *loosely coupled*.

Let's implement `get_keywords_for_movie` first:

    #!py
    def get_keywords_for_movie(url):
        """Return a list of keywords associated with *movie*."""
        keywords = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        tables = soup.find_all('table', class_='dataTable')
        table = tables[0]
        return [td.text for tr in table.find_all('tr') for td in tr.find_all('td')]

We're using both `requests` and `BeautifulSoup`, so we need to install them with
pip. Now would be a good time to list the project's requirements via `pip freeze
requirements.txt` and commit them. This way, we can always create a virtual
environment and install exactly the packages and versions we need to run the
application.

The list comprehension that is returned may look odd, but it's simply doing an
additional, *nested* iteration over the results of the first and using the
elements from the nested iteration. With list comprehensions, you can chain as
many `for` statements as you'd like.

The last step is the implementation of `get_top_grossing_movie_links`:

    #!py
    def get_top_grossing_movie_links(url):
        """Return a list of tuples containing the top grossing movies of 2013 and link to their IMDB
        page."""
        response = requests.get(url)
        movies_list = []
        for each_url in BeautifulSoup(response.text).select('.title a[href*="title"]'):
            movie_title = each_url.text 
            if movie_title != 'X':
                movies_list.append((movie_title, each_url['href']))
        return movies_list

Reasonably straightforward. The `if movie_title != 'X'` was due to my `select`
being a bit too permissive. Rather than try to get it *just* right, I simply filter out
the links that are bogus with the `if` statement.

Here is the contents of `imdb.py` in their entirety:

    #!py
    """Script to gather IMDB keywords from 2013's top grossing movies."""
    import sys
    import requests
    from bs4 import BeautifulSoup
    import csv

    URL = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us,desc&start=1&year=2013,2013"

    def get_top_grossing_movie_links(url):
        """Return a list of tuples containing the top grossing movies of 2013 and link to their IMDB
        page."""
        response = requests.get(url)
        movies_list = []
        for each_url in BeautifulSoup(response.text).select('.title a[href*="title"]'):
            movie_title = each_url.text 
            if movie_title != 'X':
                movies_list.append((movie_title, each_url['href']))
        return movies_list



    def get_keywords_for_movie(url):
        """Return a list of keywords associated with *movie*."""
        keywords = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        tables = soup.find_all('table', class_='dataTable')
        table = tables[0]
        return [td.text for tr in table.find_all('tr') for td in tr.find_all('td')]


    def main():
        """Main entry point for the script."""
        movies = get_top_grossing_movie_links(URL)
        with open('output.csv', 'w') as output:
            csvwriter = csv.writer(output)
            for title, url in movies:
                keywords = get_keywords_for_movie('http://www.imdb.com{}keywords/'.format(url))
                csvwriter.writerow([title, keywords])


    if __name__ == '__main__':
        sys.exit(main())

The application, which began as a blank editor window, is now complete. Running
it generates `output.csv`, containing exactly what we'd hoped for. With a
script of this length, I wouldn't write tests as the output of the script *is*
the test. However, it would certainly be possible (since our functions are
*loosely coupled*) to test each function in isolation.

## Wrapping Up

Hopefully, you now have a plan of attack when faced with starting a Python project
from scratch. While everyone has their own method of starting a project, mine is
just as likely to work for you as any other, so give it a try. As always, if you
have any questions, feel free to ask in the comments or email me at 
[jeff@jeffknupp.com](mailto:jeff@jeffknupp.com).
