# Open-Sourcing a Python Project The Right Way

Most Python developers have written at least *one* tool, script, 
library or framework that others would find useful. My goal in this article
is to make the process of open-sourcing existing Python code as clear 
and painless as possible. And I don't simply mean, "create GitHub repo,
`git push`, post on Reddit, and call it a day." By the end of this article,
you'll be able to take an existing code base and transform it into an open source 
project that encourages both use *and* contribution.

While every project is different, there are some parts of the process of
open-sourcing existing code that are common to *all* Python projects. 
In the vein of another popular series I've written, ["Starting a Django Project The Right Way,"](http://www.jeffknupp.com/blog/2012/10/24/starting-a-django-14-project-the-right-way/) I'll outline the steps I've 
found to be necessary when open-sourcing a Python project.

## Tools and Concepts

In particular, there are a number of tools and concepts I've found 
useful or necessary. I'll cover each of the topics below, including the 
precise commands you'll need to run and configuration values you'll need to
set. The goal is to make the entire process clear and simple.

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

## Conclusion

We've now covered all of the commands, tools, and services that go into open
sourcing an existing Python package. Sure, you could have just thrown it on
GitHub and said, "install it yourself," *but no one would have.* And you
wouldn't *really* have Open Source Software; you'd simply have "free code."

What's more, you likely never would have attracted outside contributors to your 
project. By setting up your project in the manner outlined here, you've created 
an easy to maintain Python package that encourages *both use and contribution*.
And that, after all, is the true spirit of Open Source Software, is it not?
