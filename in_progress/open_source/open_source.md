# Open Sourcing a Python Project The Right Way

Most developers accumulate a personal library of tools they've written throughout 
their career. They range from little scripts to not so little libraries, but are 
generally things that the developer wrote (ostensibly) because nothing existed 
to solve his or her particular problem. Many of these tools might be useful to
other developers, but they never see the light of day. 

I've released a few open source tools. In doing so, I've noticed a series of steps 
common to the Python projects. I'd like to make more clear the steps to open-sourcing 
Python projects in a way that encourages both use of and contribution to the project. In the vein of 
another popular series I've written, ["Starting a Django Project The Right Way,"](http://www.jeffknupp.com/blog/2012/10/24/starting-a-django-14-project-the-right-way/) I'll outline the steps I've 
found to be necessary when creating an open-sourcing a Python project.

## Tools and Concepts

In particular, there are a number of things I've found necessary for
successfully open-sourcing a Python project:

1. Project layout (directory structure)
1. `setuptools` and the `setup.py` file
1. [git](http://www.git-scm.com) for version control
1. [GitHub](http://www.github.com) for project management
    1. GitHub's "Issues" for the following:
        1. bug tracking
        1. feature requests
        1. planned features
        1. release/version management
1. [git-flow](http://nvie.com/posts/a-successful-git-branching-model/) for git workflow
1. [py.test](http://www.pytest.org) for unit testing
1. [Sphinx](http://www.sphinx-doc.org) for auto-generated HTML documentation
1. [TravisCI](https://travis-ci.org/) for continuous testing integration
1. [ReadTheDocs](https://readthedocs.org) for continuous documentation integration
1. [coverage.io](http://coverage.io) for test coverage continuous integration


*Note: In this article, I'll assume you have an existing code base you're looking to open source (and I'll assume you're using Python 2.7.x, but the steps are largely the same if you're using Python 3.x).*

## Project Layout

*include 'project_layout.md'*

## `setuptools` and the `setup.py` File

*include setup_py.md*

## Source Control With Git, Project Management with GitHub

*include git_github.md*

## A Sensible git Workflow With git-flow

*include git_flow.md*

## `virtualenv` and `virtualenvwrapper`

*include virtualenv.md*

## Testing With py.test

*include pytest.md*

## Documentation with *Sphinx*

*include sphinx.md*

## PyPI

*include pypi.md*

## Continuous Integration with TravisCI

*include travisci.md*

## ReadTheDocs for Continuous Documentation Integration

*include readthedocs.md*
