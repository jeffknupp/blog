# Open Sourcing a Python Project The Right Way

Most developers accumulate a personal library of tools they've written throughout 
their career. They range from little scripts to not so little libraries, but are 
generally things that the developer wrote (ostensibly) because nothing existed 
to solve his or her particular problem. Many of these tools might be useful to
other developers, but they never see the light of day. 

I've released a few open source tools, many of which were Python-based. In doing so, 
I've noticed a series of steps common to Python projects. I'd like to make more clear
the steps to open-sourcing Python projects in a way that encourages both use and 
contribution. In the vein of another popular series I've 
written, "Starting a Django Project The Right Way," I'll outline the steps I've 
found to be necessary when creating an open-sourcing a Python project.

## Tools and Concepts

In particular, there are a number of things I've found necessary for
successfully open-sourcing a Python project:

1. Project layout (directory structure)
1. [git](http://www.git-scm.com) for version control
1. [GitHub](http://www.github.com) for project management
    1. GitHub's "Issues" for the following:
        1. bug tracking
        1. feature requests
        1. planned features
        1. release/version management
1. [Sphinx](http://www.sphinx-doc.org) for auto-generated HTML documentation
1. [py.test](http://www.pytest.org) for unit testing
1. [TravisCI](https://travis-ci.org/) for continuous testing integration
1. [ReadTheDocs](https://readthedocs.org) for continuous documentation integration
1. [coverage.io](http://coverage.io) for test coverage continuous integration


*Note: In this article, I'll assume you have an existing code base you're looking to open source (and I'll assume you're using Python 2.7.x, but the steps are largely the same if you're using Python 3.x).*

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

## Source Control With Git, Project Management with GitHub

In "Starting a Django Project The Right Way," I suggest either git
and mercurial for version control. For a project meant to be both shared and
contributed to, there's really only one choice: git. In fact, I'll go so far as
to say that not only is the use of git necessary, you'll also need to use
[GitHub](http://www.github.com) to maintain your project if you want people to
actually use and contribute to it. 

It's not meant to be an inflamitory statement (though no doubt many will 
take issue with it). Rather, for better or worse, git
and [GitHub](http://www.github.com) have become the de-facto standard for
managing Open Source projects. GitHub is the site potential contributors are 
most likely to be registered on and familiar with. That, I believe, is not a
trivial thing.


#### Create a `README.md` File

The project description for repos on GitHub is taken from a file in the root
directory of the project: `README.md`. This file should contain the following
pieces of information:

* A description of your project
* Links to the project's ReadTheDocs page
* A TravisCI button showing the state of the build
* A "quickstart" version of installing and using your project
* A list of non-Python dependencies (if any) and how to install them

It may sound silly, but this is an important file. It's quite likely to be the first
thing both prospective users *and* contributors read about your project. Take
some time to write a clear description and make use of GFM (GitHubFlavoredMarkdown)
to make it look somewhat attractive. You can actually create/edit this 
file right on GitHub with a live-preview editor if you're not comfortable 
writing documents in raw Markdown.

We haven't yet covered the second and third items in the list yet (ReadTheDocs
and TravisCI). You'll find these discussed below.

#### A Sensible Git Workflow With Git-Flow

To make things easier on both yourself and contributors, we'll be using the
very popular [git-flow](http://nvie.com/posts/a-successful-git-branching-model/)
model of branching. In short, the `develop` branch off of which branches for new features
should be made. Once a feature is complete, the changes are merged back in to
`develop` and the feature branch is deleted. Updating `master` is done through
the creation of a `release`. 

Install git-flow by following the instructions for your platform [here](https://github.com/nvie/gitflow/wiki/Installation).

Once installed, you can migrate your existing project with the command

    #!bash
    $ git flow init

You'll be asked a number of configuration questions by the script. The default values suggested by 
git-flow are fine to use. You may notice your default branch is set to `develop`. More 
on that in a moment. Let's take a step back and describe the git-flow... erm, flow, in 
a bit more detail. The easiest way to do so is to discuss the various branches
and *types* of branches in the model.

##### Master

`master` is always "production ready" code. Commits are never made directly to `master`. Rather, 
code on `master` only gets there after a production release branch is created
and "finished" (more on that in a sec). Thus the code on `master` is always able
to be released to production. Also, `master` is always in a predictable state,
so you never need to worry if `master` (and thus production) has changes one of
your other branches doesn't.

##### Develop

Most of your work is done on the `develop` branch. This branch contains all of the completed features and
bugfixes yet to be released; nightly builds or continuous integration servers should target `develop`,
as it represents the code that will be included in the next release.

For one-off commits, feel free to commit to `develop` directly. 

##### Feature

For larger features, a `feature` branch should be created. `feature` branches are created off of
`develop`. They can be small enhancements for the next release or further out
changes that, nonetheless, need to be worked on now. To start work on a new
feature, use:

    #!bash
    $ git flow feature start <feature name>

This creates a new branch: `feature/<feature name>`. Commits are then made to this branch 
as normal. When the feature is complete *and ready to be released to production*, it 
should be merged back into develop using the following command:


    #!bash
    $ git flow feature finish <feature name>

This merges the code into `develop` and deletes the `feature/<feature name>` branch.

##### Release

A `release` branch is created from `develop` when you're ready to begin a
production release. Create one using the following command:

    
    #!bash
    $ git flow release start <release number>

Note that this is the first time a version number for the release is created.
All completed and ready to be released features must already be on `develop`
(and thus `feature finish`'ed). After your release branch is created, release
your code. Any small bug fixes needed after the release are made directly to the
`release/<release number>` branch. Once it has settled down and no more bug
fixes seem necessary, run the following command:

    #!bash
    $ git flow release finish <release number>

This merges your `release/<release number>` changes back into both `master`
*and* `develop`, meaning you never need to worry about either of those branches
lacking changes that are in production (perhaps as the result of a quick bug
fix).

##### Hotfix

While potentially useful, `hotfix` branches are, I would guess, little used in
the real world. A `hotfix` is like a `feature` branch off of `master`: if you've
already closed a `release` branch but realize there are vital changes that need
to be released, create a `hotfix` branch off of `master` (at the tag created
during `$ git flow release finish <release number>`) like so:


    #!bash
    $ git flow hotfix start <release number>

After you make your changes and bump your version number, finalize the `hotfix` via

    #!bash
    $ git flow hotfix finish <release number>

This, like a `release` branch (since it essentially *is* a type of release
branch), commits the changes to both `master` and `develop`.

The reason I assume they're rarely used is because there is already a mechanism
for making changes to released code: committing to an un-`finish`ed release
branch. Sure, in the beginning, teams may `git flow release finish ...` too
early, only to find they need to make some quick changes the next day. Over
time, though, they'll settle on a reasonable amount of time for a `release`
branch to remain open and, thus, won't have a need for `hotfix` branches. The
only *other* time you would need a `hotfix` branch is if you needed a new
"feature" in productioni immediately, without picking up the changes already in
`develop`. That strikes me as something that happens (hopefully) very rarely.

## `virtualenv` and `virtualenvwrapper`

Ian Bicking's `virtualenv` tool has become the de-facto standard mechanism for
isolating Python environments. Its purpose is simple: if you have a number of
Python projects on a single machine, each with different dependencies (perhaps
with dependencies on different versions of the same package), managing the dependencies in a
single Python installation is nigh impossible. 

`virtualenv` creates "virtual" Python installations, each with their 
own, segregated, `site-packages`. `distribute` and `pip` are also 
installed in such a way that `pip install` correctly installs packages 
to the `virtualenv` rather than the system Python installation. Switching back 
and forth between your `virtualenv` is a one-command process.

A separate tool, Doug Hellmann's `virtualenvwrapper`, makes creating and managing multiple 
`virtualenv`s easier. Let's go ahead and install both now:

    #!bash
    $ pip install `virtualenvwrapper`
    ...
    Successfully installed `virtualenvwrapper` `virtualenv` `virtualenv`-clone stevedore
    Cleaning up...

As you can see, the latter has a dependency on the former, so simply installing
`virtualenvwrapper` is sufficient. Note that if you're using Python 
3, [PEP-405](http://www.python.org/dev/peps/pep-0405/), which gives Python 
native support for virtual environments through the `venv` package 
and `pyvenv` command, was implemented in Python 3.3. You should use that instead
of the tools mentioned above.

Once you've installed `virtualenvwrapper`, you'll need to add a line to your
`.zhsrc` file (or `.bashrc` file for bash users):

    #!bash
    $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.zshrc

This adds a number of useful commands to your shell (remember to `source` your
`.zshrc` to actually make them available for the first time). While you can create a
`virtualenv` directly with the `mkvirtualenv` command, creating a *"project"*
using `mkproject [OPTIONS] DEST_DIR` is usually more useful. Since we have 
an existing project, however, we'll simply create a new `virtualenv` for our
project. We can do this with a simple command:

    $ mkvirtualenv ossproject

    New python executable in ossproject/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    (ossproject)$ 

You'll notice your shell prompt is now prepended by the name of your `virtualenv`
(which I called "ossproject", but obviously you can use whatever name you'd
like). Now anything installed via `pip install` is installed to the
`site-packages` of your `virtualenv`. 

To stop working on your project and switch back to the system installation, use 
the `deactivate` command. You should see the `virtualenv` name that was prepended 
to your shell prompt dissapear. To resume work on your project, run `$ workon
<project name>` and you'll be back in your `virtualenv`.

Aside from simply creating the `virtualenv` for your project, you'll use it to
do one more thing: generate your `requirements.txt` file. `pip` is capable of
installing all of project's dependencies by using a requirements file and the
`-r` flag. To create this file, run the following command within your `virtualenv`
(once your code is working with the `virtualenv`, that is):

    #!bash
    (ossproject)$ pip freeze > requirements.txt

You'll get a nice list of all of the requirements for your project, which can
later be used by the setup.py file to list your dependencies. One note here: I
often change the '==' to '>=' in `requirements.txt` to say "any version of this
package after the one I'm working on." Whether or not you should/need to do this
is project specific, but I just thought I'd point it out.

Commit `requirements.txt` to your git repo, as a number of tools/services we'll
see later make use of it.

## PyPI and `setuptools`
=======
>>>>>>> Stashed changes

TODO

## Testing With py.test

In the Python automated testing ecosystem, there are two main alternatives to
the (quite usable) Python standard library `unittest` package:
[nose](http://www.nosetest.org) and [py.test](http://www.pytest.org). Both 
extend `unittest` to make it easier to work with while adding additional
functionality. Truthfully, either is a fine choice. I happen to prefer
`py.test` for a few reasons:

* Support for setuptools/distutils projects
    * `python setup.py test` still works
* Support for "normal" `assert` statements (rather than needing to remember all the jUnit-style assert functions)
* Less boilerplate
* Support for multiple testing styles
    * `unittest`
    * `doctest`
    * nose tests

#### Note

If you already have an automated testing solution, feel free to continue using
it and skip this section. Be warned that later sections may assume testing is
done using py.test, which may affect configuration values.

#### Test Setup

In the `test` directory, wherever you decided it should live, create a file called
`test_<project_name>.py`. py.test's test discovery mechanism will treat any file
with the `test_` prefix as a test file (unless told otherwise).

What you put in that file is largely up to you. Writing tests is a giant topic 
and outside of the scope of this article. The important thing, however, is that the
tests are useful to both you *and potential contributors*. It should be clear
what functionality each test is exercising. Tests should be written in the same
"style" so that a potential contributor doesn't have to guess which of the three
styles of testing used in your project he/she should use.

The main goal is for the tests to be easy to run. There should be a single
command to run "all" of the tests. If you need to test against multiple
interpreters, consider using [tox](http://tox.readthedocs.org/en/latest/).

#### Test Coverage

Automated test coverage is a contentious topic. Some believe it to be a
meaningless metric that gives false security. Others find it genuinely useful.
At the very least, I would suggest if you already have tests and have *never*
checked your test coverage, do so now as an exercise. 

With py.test, we can make use of Ned Bechteld ### FIXME #### [coverage](http://www.FIXME.com)
tool. To do so, `pip install pytest-cov`. If you previously ran your tests like
this:

    #!bash
    $ py.test

you can generate test coverage reports by passing a few addtional flags. Below
is an example of running `sandman`

    #!bash
    $ py.test --cov=path/to/package 
    $ py.test --cov=path/to/package --cov-report=term --cov-report=html                              ⏎ ✭
    ====================================================== test session starts =======================================================
    platform darwin -- Python 2.7.5 -- pytest-2.3.5
    plugins: cov
    collected 23 items

    sandman/test/test_sandman.py .......................
    ---------------------------------------- coverage: platform darwin, python 2.7.5-final-0 -----------------------------------------
    Name                           Stmts   Miss  Cover
    --------------------------------------------------
    sandman/__init__                   5      0   100%
    sandman/exception                 10      0   100%
    sandman/model                     48      0   100%
    sandman/sandman                  142      0   100%
    sandman/test/__init__              0      0   100%
    sandman/test/models               29      0   100%
    sandman/test/test_sandman        114      0   100%
    --------------------------------------------------
    TOTAL                            348      0   100%
    Coverage HTML written to dir htmlcov

    =================================================== 23 passed in 1.14 seconds ====================================================
=======

### Documentation with *Sphinx*

[Sphinx](http://www.sphinx-doc.org) is a tool by the [pocoo](http://www.pocoo.org/) folks. It's used to 
generate the Python's official documentation and the documentation for almost all other popular Python 
packages. It was written with idea of making auto-generation of HTML documentation from Python code as easy as possible.

Be sure to install Sphinx *in your virtualenv*, since documentation will be a
versioned artifact in your project and different versions of sphinx may generate
different HTML output. By doing so, you can "upgrade" your documentation in a
controlled manner.
