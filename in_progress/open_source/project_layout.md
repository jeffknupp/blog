## Project Layout

When setting up a project, the *layout* (or *directory structure*) is important
to get right. A sensible layout means that potential contributors don't have to
spend forever hunting for a piece of code; file locations are intuitive. Since
we're dealing with an existing project, it means you'll probably need to move
some stuff around.

Let's start at the top. Most projects have a number of top-level files (like
`setup.py`, `README.md`, `requirements.txt`, etc). There are then three
directories that *every* project should have:

1. A `docs` directory containing project documentation
1. A directory named with the project's name which stores the actual Python package
1. A `test` directory in one of two places
    1. Under the package directory containing test code and resources
    1. As a stand-alone top level directory

To get a better sense of how your files should be organized, here's a simplified snapshot
of the layout for one of my projects, [sandman](http://www.github.com/jeffknupp/sandman):

    #!bash
    $ pwd
    ~/code/sandman
    $ tree
    .
    ├── LICENSE
    ├── README.md
    ├── TODO.md
    ├── docs
    │   ├── conf.py
    │   ├── generated
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── modules.rst
    │   ├── quickstart.rst
    │   └── sandman.rst
    ├── requirements.txt
    ├── sandman
    │   ├── __init__.py
    │   ├── exception.py
    │   ├── model.py
    │   ├── sandman.py
    │   └── test
    │       ├── models.py
    │       └── test_sandman.py
    └── setup.py

    4 directories, 17 files

As you can see, there are some top level files, a `docs` directory (`generated`
is an empty directory where sphinx will put the generated documentation), a
`sandman` directory, and a `test` directory under `sandman`.


