# Creating an Open Source Python Library The Right Way

Most developers accumulate a personal library of tools they've written throughout 
their career. They range from little scripts to not so little libraries, but are 
generally things that the developer wrote because (ostensibly) nothing existed 
to solve his or her particular problem. Many of these tools might be useful to
other developers, but they never see the light of day. 

#Sometimes, especially when written at/for work, there are reasons outside the 
#developer's control that prevent their tools from being open sourced. Other 
#times, it's a matter of time committment or perceived value. But many times,
#a developer 

I'd like to make the road to Open-Sourcing Python projects more clear. 
I've released a few open source tools, many of which were Python-based. In doing
so, I've noticed a series of steps common to those projects done in Python. In
the vein of another popular series I've written, "Starting a Django Project The
Right Way," I'll outline the steps I've found to be necessary when creating an
Open Source Python project.

## Before We Begin

In this article, we'll assume you have an existing code base you're looking to 
open source (I'll assume Python 2.7.x, but the steps are largely the same with 
Python 3). With an existing code base, you'll need to do a bit of retro-fitting.
Before we start, though, there are a few technologies you'll need to make yourself familiar
with. 

#### virtualenv and virtualenvwrapper

Ian Bicking's virtualenv tool has become the de-facto standard mechanism for
isolating Python environments. Its purpose is simple: if you have a number of
Python projects on a single machine, each with different dependencies (perhaps
on different versions of the same package), managing the dependencies in a
single Python installation is nigh impossible. 

virtualenv creates "virtual" Python installations, each with their 
own, segregated, `site-packages`.  `distribute` and `pip` are also 
installed in such a way that `pip install` correctly installs packages 
to the virtualenv rather than the system Python installation. Switching back 
and forth between your virtualenv is a one-command process.

A separate tool, Doug Hellmann's virtualenvwrapper, makes creating and managing multiple 
virtualenvs easier. Let's go ahead and install both now:

    #!bash
    $ pip install virtualenvwrapper
    ...
    Successfully installed virtualenvwrapper virtualenv virtualenv-clone stevedore
    Cleaning up...

As you can see, the latter has a dependency on the former, so simply installing
virtualenvwrapper is sufficient. Note that if you're using Python 
3, [PEP-405](http://www.python.org/dev/peps/pep-0405/), which gives Python 
native support for virtual environments through the `venv` package 
and `pyvenv` command, was implemented in Python 3.3. You should use that instead
of the tools mentioned above.

Once you've installed virtualenvwrapper, you'll need to add a line to your
`.zhsrc` file (or `.bashrc` file for bash users):

    #!bash
    $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.zshrc

This adds a number of useful commands to your shell (remember to `source` your
`.zshrc` to actually make them available for the first time). While you can create a
virtualenv directly with the `mkvirtualenv` command, creating a *"project"*
using `mkproject [OPTIONS] DEST_DIR` is usually more useful. Since we have 
an existing project, however, we'll simply create a new virtualenv for our
project. We can do this with a simple command:

    $ mkvirtualenv ossproject

    New python executable in ossproject/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    (ossproject)$ 

You'll notice your shell prompt is now prepended by the name of your virtualenv
(which I called "ossproject", but obviously you can use whatever name you'd
like). Now anything installed via `pip install` is installed to the
`site-packages` of your virtualenv. 

To stop working on your project and switch back to the system installation, use 
the `deactivate` command. You should see the virtualenv name that was prepended 
to your shell prompt dissapear. To resume work on your project, run `$ workon
<project name>` and you'll be back in your virtualenv.

## Source Control With Git

In "Starting a Django Project The Right Way," I suggest either git
and mercurial for version control. For a project meant to be both shared and
contributed to, there's really only one choice: git. In fact, I'll go so far as
to say that not only is the use of git necessary, you'll also need to use
[GitHub](http://www.github.com) to maintain your project if you want people to
actually use and contribute to it. 

It's not meant to be an inflamitory statement (though no doubt many will 
take issue with it). Rather, for better or worse, git
and [GitHub](http://www.github.com) have become the de-facto standard for
managing Open Source projects. GitHub is the site potential users and
contributors are most likely to be registered at and most likely to be familiar
with the workflow.

#### A Sensible Git Workflow With Git-Flow

To make things easier on both yourself and contributors, we'll be using the
very popular [git-flow](http://nvie.com/posts/a-successful-git-branching-model/)
model of branching. In short, the `develop` branch off of which branches for new features
should be made. Once a feature is complete, the changes are merged back in to
`develop` and the feature branch is deleted. Updating `master` is done through
the creation of a `release`. Install git-flow by following the instructions for your platform [here](https://github.com/nvie/gitflow/wiki/Installation).

Once installed, you can migrate your existing project with the command

    #!bash
    $ git flow init

The default values suggested by git-flow are fine to use.

#### Managing Your Project on GitHub


